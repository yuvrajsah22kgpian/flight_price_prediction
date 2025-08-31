# ✈️ Flight Price Prediction

A machine learning web application that predicts flight prices using XGBoost regression model. Built with React frontend and FastAPI backend.

## 🚀 Features

- **Real-time Price Prediction**: Get instant flight price predictions based on various parameters
- **Interactive Web Interface**: Modern React-based UI with form validation
- **RESTful API**: FastAPI backend with automatic API documentation
- **Advanced ML Pipeline**: Sophisticated feature engineering and preprocessing
- **CORS Support**: Cross-origin resource sharing enabled for frontend-backend communication

## 🏗️ Project Structure

```
flight_price_prediction_react_fastapi/
├── Backend/                 # FastAPI backend
│   ├── Data/               # Dataset and model files
│   │   ├── flight_price.csv
│   │   ├── train.csv
│   │   ├── val.csv
│   │   └── test.csv
│   ├── main.py             # FastAPI application
│   ├── requirements.txt    # Python dependencies
│   ├── preprocessor.joblib # Preprocessing pipeline
│   └── xgboost-model       # Trained XGBoost model
├── frontend/               # React frontend
│   ├── src/
│   │   ├── App.jsx         # Main React component
│   │   ├── App.css         # Styling
│   │   └── main.jsx        # React entry point
│   ├── package.json        # Node.js dependencies
│   └── vite.config.mjs     # Vite configuration
└── README.md               # This file
```

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **XGBoost**: Gradient boosting library for machine learning
- **Scikit-learn**: Machine learning library for preprocessing
- **Feature-engine**: Advanced feature engineering library
- **Pandas & NumPy**: Data manipulation and numerical computing
- **Pydantic**: Data validation using Python type annotations

### Frontend
- **React 18**: Modern JavaScript library for building user interfaces
- **Vite**: Fast build tool and development server
- **CSS3**: Modern styling with responsive design

## 📋 Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn package manager

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd flight_price_prediction_react_fastapi
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd Backend

# Create virtual environment (optional but recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
```

## 🏃‍♂️ Running the Application

### 1. Start the Backend Server

```bash
# From the Backend directory
cd Backend

# Activate virtual environment (if using one)
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Start the FastAPI server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at `http://localhost:8000`

### 2. Start the Frontend Development Server

```bash
# From the frontend directory
cd frontend

# Start the development server
npm run dev
```

The frontend will be available at `http://localhost:5173`

## 📖 API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints

#### 1. Get Dropdown Options
```http
GET /dropdown-options
```

**Response:**
```json
{
  "airlines": ["Air India", "GoAir", "IndiGo", ...],
  "sources": ["Banglore", "Kolkata", "Delhi", ...],
  "destinations": ["New Delhi", "Banglore", "Kolkata", ...],
  "additional_info": ["No info", "In-flight meal not included", ...]
}
```

#### 2. Predict Flight Price
```http
POST /predict
```

**Request Body:**
```json
{
  "airline": "Air India",
  "date_of_journey": "2024-01-15",
  "source": "Banglore",
  "destination": "New Delhi",
  "dep_time": "10:30",
  "arrival_time": "12:45",
  "duration": 135,
  "total_stops": 0,
  "additional_info": "No info"
}
```

**Response:**
```json
{
  "predicted_price": 4500.75,
  "message": "Prediction successful"
}
```

### Interactive API Documentation

Once the backend is running, you can access:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🎯 Usage

1. **Open the Application**: Navigate to `http://localhost:5173` in your browser
2. **Fill the Form**: Enter flight details including:
   - Airline
   - Date of journey
   - Source and destination cities
   - Departure and arrival times
   - Duration (in minutes)
   - Number of stops
   - Additional information
3. **Get Prediction**: Click "Predict Price" to receive the estimated flight price
4. **View Results**: The predicted price will be displayed with a success message

## 🔧 Model Details

### Features Used
- **Airline**: Categorical feature with airline names
- **Date Features**: Extracted day, month, year, day of week
- **Time Features**: Extracted hour, minute, and time-based features
- **Route Information**: Source, destination, duration, stops
- **Additional Info**: Special information about the flight

### Preprocessing Pipeline
- **Feature Engineering**: Date/time feature extraction
- **Encoding**: One-hot encoding for categorical variables
- **Scaling**: Standard scaling for numerical features
- **Outlier Handling**: Winsorization for extreme values
- **Feature Selection**: Performance-based feature selection

### Model Performance
- **Algorithm**: XGBoost Regressor
- **Evaluation Metric**: R² Score
- **Cross-validation**: K-fold cross-validation for robust evaluation

## 🐛 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Kill process using port 8000
   lsof -ti:8000 | xargs kill -9
   ```

2. **Module Not Found Errors**
   ```bash
   # Reinstall dependencies
   pip install -r requirements.txt
   ```

3. **CORS Errors**
   - Ensure backend is running on port 8000
   - Check that frontend is making requests to correct URL

4. **Model Loading Issues**
   - Verify that `xgboost-model` and `preprocessor.joblib` files exist in Backend directory

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Dataset: Flight price prediction dataset
- XGBoost: For the powerful gradient boosting implementation
- FastAPI: For the excellent web framework
- React: For the frontend framework
- Feature-engine: For advanced feature engineering capabilities

## 📞 Support

If you encounter any issues or have questions, please:
1. Check the troubleshooting section above
2. Review the API documentation at `http://localhost:8000/docs`
3. Open an issue on the repository

---

**Happy Predicting! ✈️💰** 