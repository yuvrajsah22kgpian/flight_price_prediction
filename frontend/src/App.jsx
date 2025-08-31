import React, { useState, useEffect } from 'react';
import './App.css';

const API_BASE_URL = 'http://localhost:8000';

function App() {
  // State for form inputs
  const [formData, setFormData] = useState({
    airline: '',
    date_of_journey: '',
    source: '',
    destination: '',
    dep_time: '',
    arrival_time: '',
    duration: '',
    total_stops: 0,
    additional_info: ''
  });

  // State for dropdown options
  const [dropdownOptions, setDropdownOptions] = useState({
    airlines: [],
    sources: [],
    destinations: [],
    additional_info: []
  });

  // State for prediction result
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Fetch dropdown options on component mount
  useEffect(() => {
    fetchDropdownOptions();
  }, []);

  const fetchDropdownOptions = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/dropdown-options`);
      if (!response.ok) {
        throw new Error('Failed to fetch dropdown options');
      }
      const data = await response.json();
      setDropdownOptions(data);
    } catch (err) {
      setError('Failed to load dropdown options: ' + err.message);
    }
  };

  const handleInputChange = (e) => {
    const { name, value, type } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'number' ? parseInt(value) || 0 : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setPrediction(null);

    try {
      const response = await fetch(`${API_BASE_URL}/predict`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Prediction failed');
      }

      const data = await response.json();
      setPrediction(data);
    } catch (err) {
      setError('Prediction failed: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>✈️ Flight Price Prediction</h1>
        <p>AWS SageMaker Model</p>
      </header>

      <main className="main-content">
        <div className="form-container">
          <form onSubmit={handleSubmit} className="prediction-form">
            <div className="form-row">
              <div className="form-group">
                <label htmlFor="airline">Airline:</label>
                <select
                  id="airline"
                  name="airline"
                  value={formData.airline}
                  onChange={handleInputChange}
                  required
                >
                  <option value="">Select Airline</option>
                  {dropdownOptions.airlines.map(airline => (
                    <option key={airline} value={airline}>{airline}</option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label htmlFor="date_of_journey">Date of Journey:</label>
                <input
                  type="date"
                  id="date_of_journey"
                  name="date_of_journey"
                  value={formData.date_of_journey}
                  onChange={handleInputChange}
                  required
                />
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="source">Source:</label>
                <select
                  id="source"
                  name="source"
                  value={formData.source}
                  onChange={handleInputChange}
                  required
                >
                  <option value="">Select Source</option>
                  {dropdownOptions.sources.map(source => (
                    <option key={source} value={source}>{source}</option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label htmlFor="destination">Destination:</label>
                <select
                  id="destination"
                  name="destination"
                  value={formData.destination}
                  onChange={handleInputChange}
                  required
                >
                  <option value="">Select Destination</option>
                  {dropdownOptions.destinations.map(destination => (
                    <option key={destination} value={destination}>{destination}</option>
                  ))}
                </select>
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="dep_time">Departure Time:</label>
                <input
                  type="time"
                  id="dep_time"
                  name="dep_time"
                  value={formData.dep_time}
                  onChange={handleInputChange}
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="arrival_time">Arrival Time:</label>
                <input
                  type="time"
                  id="arrival_time"
                  name="arrival_time"
                  value={formData.arrival_time}
                  onChange={handleInputChange}
                  required
                />
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="duration">Duration (mins):</label>
                <input
                  type="number"
                  id="duration"
                  name="duration"
                  value={formData.duration}
                  onChange={handleInputChange}
                  min="1"
                  step="1"
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="total_stops">Total Stops:</label>
                <input
                  type="number"
                  id="total_stops"
                  name="total_stops"
                  value={formData.total_stops}
                  onChange={handleInputChange}
                  min="0"
                  step="1"
                  required
                />
              </div>
            </div>

            <div className="form-row full-width">
              <div className="form-group">
                <label htmlFor="additional_info">Additional Info:</label>
                <select
                  id="additional_info"
                  name="additional_info"
                  value={formData.additional_info}
                  onChange={handleInputChange}
                  required
                >
                  <option value="">Select Additional Info</option>
                  {dropdownOptions.additional_info.map(info => (
                    <option key={info} value={info}>{info}</option>
                  ))}
                </select>
              </div>
            </div>

            <button 
              type="submit" 
              className="predict-button"
              disabled={loading}
            >
              {loading ? 'Predicting...' : 'Predict Price'}
            </button>
          </form>

          {error && (
            <div className="error-message">
              <p>{error}</p>
            </div>
          )}

          {prediction && (
            <div className="prediction-result">
              <h3>Prediction Result</h3>
              <div className="price-display">
                <span className="price">₹{prediction.predicted_price.toLocaleString('en-IN')}</span>
                <span className="currency">INR</span>
              </div>
              <p>{prediction.message}</p>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

export default App;
