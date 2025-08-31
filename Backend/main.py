import os
import pickle
import warnings
import joblib
import numpy as np
import pandas as pd
import xgboost as xgb
import sklearn
from sklearn.metrics import r2_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics.pairwise import rbf_kernel
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import (
    OneHotEncoder,
    OrdinalEncoder,
    StandardScaler,
    MinMaxScaler,
    PowerTransformer,
    FunctionTransformer
)

from feature_engine.outliers import Winsorizer
from feature_engine.datetime import DatetimeFeatures
from feature_engine.selection import SelectBySingleFeaturePerformance
from feature_engine.encoding import (
    RareLabelEncoder,
    MeanEncoder,
    CountFrequencyEncoder
)

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime, date, time
from typing import Optional, List

sklearn.set_config(transform_output="pandas")

# Initialize FastAPI app
app = FastAPI(title="Flight Price Prediction API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev server ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class FlightPredictionRequest(BaseModel):
    airline: str
    date_of_journey: str  # Format: YYYY-MM-DD
    source: str
    destination: str
    dep_time: str  # Format: HH:MM
    arrival_time: str  # Format: HH:MM
    duration: int  # in minutes
    total_stops: int
    additional_info: str

class FlightPredictionResponse(BaseModel):
    predicted_price: float
    message: str

class DropdownOptions(BaseModel):
    airlines: List[str]
    sources: List[str]
    destinations: List[str]
    additional_info: List[str]

# All the preprocessing classes and functions from your original code
class RBFPercentileSimilarity(BaseEstimator, TransformerMixin):
    def __init__(self, variables=None, percentiles=[0.25, 0.5, 0.75], gamma=0.1):
        self.variables = variables
        self.percentiles = percentiles
        self.gamma = gamma

    def fit(self, X, y=None):
        if not self.variables:
            self.variables = X.select_dtypes(include="number").columns.to_list()

        self.reference_values_ = {
            col: (
                X
                .loc[:, col]
                .quantile(self.percentiles)
                .values
                .reshape(-1, 1)
            )
            for col in self.variables
        }

        return self

    def transform(self, X):
        objects = []
        for col in self.variables:
            columns = [f"{col}_rbf_{int(percentile * 100)}" for percentile in self.percentiles]
            obj = pd.DataFrame(
                data=rbf_kernel(X.loc[:, [col]], Y=self.reference_values_[col], gamma=self.gamma),
                columns=columns
            )
            objects.append(obj)
        return pd.concat(objects, axis=1)

# Preprocessing functions
def is_north(X):
    columns = X.columns.to_list()
    north_cities = ["Delhi", "Kolkata", "Mumbai", "New Delhi"]
    return (
        X
        .assign(**{
            f"{col}_is_north": X.loc[:, col].isin(north_cities).astype(int)
            for col in columns
        })
        .drop(columns=columns)
    )

def part_of_day(X, morning=4, noon=12, eve=16, night=20):
    columns = X.columns.to_list()
    X_temp = X.assign(**{
        col: pd.to_datetime(X.loc[:, col]).dt.hour
        for col in columns
    })

    return (
        X_temp
        .assign(**{
            f"{col}_part_of_day": np.select(
                [X_temp.loc[:, col].between(morning, noon, inclusive="left"),
                 X_temp.loc[:, col].between(noon, eve, inclusive="left"),
                 X_temp.loc[:, col].between(eve, night, inclusive="left")],
                ["morning", "afternoon", "evening"],
                default="night"
            )
            for col in columns
        })
        .drop(columns=columns)
    )

def duration_category(X, short=180, med=400):
    return (
        X
        .assign(duration_cat=np.select([X.duration.lt(short),
                                        X.duration.between(short, med, inclusive="left")],
                                       ["short", "medium"],
                                       default="long"))
        .drop(columns="duration")
    )

def is_over(X, value=1000):
    return (
        X
        .assign(**{
            f"duration_over_{value}": X.duration.ge(value).astype(int)
        })
        .drop(columns="duration")
    )

def is_direct(X):
    return X.assign(is_direct_flight=X.total_stops.eq(0).astype(int))

def have_info(X):
    return X.assign(additional_info=X.additional_info.ne("No Info").astype(int))

# Global variables to store training data and models
training_data = None
preprocessor = None
model = None

def load_models():
    """Load the preprocessor and model"""
    global training_data, preprocessor, model
    
    try:
        # Load training data to get unique values for dropdowns
        training_data = pd.read_csv("Data/train.csv")
        
        # Load preprocessor
        preprocessor = joblib.load("preprocessor.joblib")
        
        # Load XGBoost model
        with open("xgboost-model", "rb") as f:
            model = pickle.load(f)
            
    except Exception as e:
        print(f"Error loading models: {e}")
        return False
    
    return True

# Load models on startup
@app.on_event("startup")
async def startup_event():
    success = load_models()
    if not success:
        print("Warning: Could not load models. Some endpoints may not work.")

@app.get("/")
async def root():
    return {"message": "Flight Price Prediction API is running!"}

@app.get("/dropdown-options", response_model=DropdownOptions)
async def get_dropdown_options():
    """Get unique values for dropdown menus"""
    if training_data is None:
        raise HTTPException(status_code=500, detail="Training data not loaded")
    
    try:
        return DropdownOptions(
            airlines=sorted(training_data.airline.unique().tolist()),
            sources=sorted(training_data.source.unique().tolist()),
            destinations=sorted(training_data.destination.unique().tolist()),
            additional_info=sorted(training_data.additional_info.unique().tolist())
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting dropdown options: {str(e)}")

@app.post("/predict", response_model=FlightPredictionResponse)
async def predict_flight_price(request: FlightPredictionRequest):
    """Predict flight price based on input parameters"""
    if preprocessor is None or model is None:
        raise HTTPException(status_code=500, detail="Models not loaded")
    
    try:
        # Create DataFrame from request
        x_new = pd.DataFrame({
            'airline': [request.airline],
            'date_of_journey': [request.date_of_journey],
            'source': [request.source],
            'destination': [request.destination],
            'dep_time': [request.dep_time],
            'arrival_time': [request.arrival_time],
            'duration': [request.duration],
            'total_stops': [request.total_stops],
            'additional_info': [request.additional_info]
        }).astype({
            col: "str"
            for col in ["date_of_journey", "dep_time", "arrival_time"]
        })
        
        # Preprocess the data
        x_new_pre = preprocessor.transform(x_new)
        
        # Make prediction
        x_new_xgb = xgb.DMatrix(x_new_pre)
        pred = model.predict(x_new_xgb)[0]
        
        return FlightPredictionResponse(
            predicted_price=float(pred),
            message=f"The predicted price is {pred:,.0f} INR"
        )
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "preprocessor_loaded": preprocessor is not None,
        "model_loaded": model is not None,
        "training_data_loaded": training_data is not None
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
