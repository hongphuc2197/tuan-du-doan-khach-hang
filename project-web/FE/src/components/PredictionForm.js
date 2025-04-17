import React, { useState } from 'react';
import axios from 'axios';

const PredictionForm = () => {
  const [formData, setFormData] = useState({
    Income: '',
    Recency: '',
    NumWebPurchases: '',
    NumCatalogPurchases: '',
    NumStorePurchases: '',
    NumWebVisitsMonth: '',
    AcceptedCmp3: '0',
    AcceptedCmp4: '0',
    AcceptedCmp5: '0',
    AcceptedCmp1: '0',
    AcceptedCmp2: '0',
  });

  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    
    try {
      const response = await axios.post('http://localhost:3001/api/predict', formData);
      setPrediction(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="prediction-form">
      <h2>Customer Prediction Form</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Income:</label>
          <input
            type="number"
            name="Income"
            value={formData.Income}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label>Recency (days since last purchase):</label>
          <input
            type="number"
            name="Recency"
            value={formData.Recency}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label>Number of Web Purchases:</label>
          <input
            type="number"
            name="NumWebPurchases"
            value={formData.NumWebPurchases}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label>Number of Catalog Purchases:</label>
          <input
            type="number"
            name="NumCatalogPurchases"
            value={formData.NumCatalogPurchases}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label>Number of Store Purchases:</label>
          <input
            type="number"
            name="NumStorePurchases"
            value={formData.NumStorePurchases}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label>Number of Web Visits per Month:</label>
          <input
            type="number"
            name="NumWebVisitsMonth"
            value={formData.NumWebVisitsMonth}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label>Accepted Campaign 3:</label>
          <select name="AcceptedCmp3" value={formData.AcceptedCmp3} onChange={handleChange}>
            <option value="0">No</option>
            <option value="1">Yes</option>
          </select>
        </div>

        <div className="form-group">
          <label>Accepted Campaign 4:</label>
          <select name="AcceptedCmp4" value={formData.AcceptedCmp4} onChange={handleChange}>
            <option value="0">No</option>
            <option value="1">Yes</option>
          </select>
        </div>

        <div className="form-group">
          <label>Accepted Campaign 5:</label>
          <select name="AcceptedCmp5" value={formData.AcceptedCmp5} onChange={handleChange}>
            <option value="0">No</option>
            <option value="1">Yes</option>
          </select>
        </div>

        <div className="form-group">
          <label>Accepted Campaign 1:</label>
          <select name="AcceptedCmp1" value={formData.AcceptedCmp1} onChange={handleChange}>
            <option value="0">No</option>
            <option value="1">Yes</option>
          </select>
        </div>

        <div className="form-group">
          <label>Accepted Campaign 2:</label>
          <select name="AcceptedCmp2" value={formData.AcceptedCmp2} onChange={handleChange}>
            <option value="0">No</option>
            <option value="1">Yes</option>
          </select>
        </div>

        <button type="submit" disabled={loading}>
          {loading ? 'Predicting...' : 'Predict'}
        </button>
      </form>

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      {prediction && (
        <div className="prediction-result">
          <h3>Prediction Result:</h3>
          <p>
            This customer is predicted to be: 
            <strong>{prediction.result === 1 ? ' Potential Customer' : ' Not a Potential Customer'}</strong>
          </p>
          {prediction.probability && (
            <p>Confidence: {(prediction.probability * 100).toFixed(2)}%</p>
          )}
        </div>
      )}
    </div>
  );
};

export default PredictionForm; 