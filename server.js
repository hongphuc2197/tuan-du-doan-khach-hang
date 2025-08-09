const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const { PythonShell } = require('python-shell');
const csv = require('csv-parser');
const fs = require('fs');
const path = require('path');

const app = express();
const port = process.env.PORT || 5001;

// Middleware
app.use(cors());
app.use(bodyParser.json());

// Root path
app.get('/', (req, res) => {
  res.json({ message: 'Welcome to Customer Prediction API' });
});

// Test route
app.get('/api/test', (req, res) => {
  res.json({ message: 'Test route working' });
});

// Test Python endpoint
app.get('/api/test-python', (req, res) => {
  const options = {
    mode: 'text',
    pythonPath: '/Users/trantuan/tuan-du-doan-khach-hang/venv/bin/python3',
    pythonOptions: ['-u'],
    scriptPath: path.join(__dirname, '../../analytics'),
  };

  console.log('Running Python script with options:', options);
  
  PythonShell.run('test_json.py', options, (err, results) => {
    if (err) {
      console.error('Error running test Python:', err);
      res.status(500).json({ error: 'Error running test Python', details: err.message });
      return;
    }

    console.log('Python script results:', results);
    
    try {
      const result = JSON.parse(results[results.length - 1]);
      res.json(result);
    } catch (error) {
      console.error('Error parsing result:', error);
      res.status(500).json({ error: 'Error parsing result', details: error.message, rawResults: results });
    }
  });
});

// Get customers list from CSV
app.get('/api/customers', (req, res) => {
  const results = [];
  const csvPath = path.join(__dirname, '../../result.csv');
  
  fs.createReadStream(csvPath)
    .pipe(csv())
    .on('data', (data) => {
      const processedData = {};
      Object.keys(data).forEach(key => {
        if (key === 'ID') {
          processedData[key] = data[key];
        } else {
          const value = data[key] === '' ? 0 : parseFloat(data[key]);
          processedData[key] = isNaN(value) ? 0 : value;
        }
      });
      
      processedData.TotalSpent = processedData.TotalSpending || 0;
      processedData.AvgPurchaseValue = processedData.AvgPurchaseValue || 0;
      
      results.push(processedData);
    })
    .on('end', () => {
      res.json(results);
    })
    .on('error', (error) => {
      console.error('Error reading CSV:', error);
      res.status(500).json({ error: 'Error reading customer data' });
    });
});

// Predict customer endpoint
app.post('/api/predict', (req, res) => {
  const options = {
    mode: 'text',
    pythonPath: '/Users/trantuan/tuan-du-doan-khach-hang/venv/bin/python3',
    pythonOptions: ['-u'],
    scriptPath: path.join(__dirname, '../../analytics'),
    args: [JSON.stringify(req.body)]
  };

  PythonShell.run('predict.py', options, (err, results) => {
    if (err) {
      console.error('Error running prediction:', err);
      res.status(500).json({ error: 'Error running prediction', details: err.message });
      return;
    }
    
    try {
      const prediction = JSON.parse(results[0]);
      res.json(prediction);
    } catch (error) {
      console.error('Error parsing prediction result:', error);
      res.status(500).json({ error: 'Error parsing prediction result', details: error.message });
    }
  });
});

// Analytics endpoint - simplified
app.get('/api/analytics', (req, res) => {
  // Trả về dữ liệu tĩnh thay vì chạy Python script
  const analytics = {
    status: "success",
    data: {
      total_customers: 2240,
      total_features: 16,
      accuracy: 0.8504,
      missing_values: 24,
      response_distribution: {
        positive: 0.149107,
        negative: 0.850893
      },
      feature_importance: [
        { Feature: "Recency", Importance: 0.119633 },
        { Feature: "MntWines", Importance: 0.114521 },
        { Feature: "Income", Importance: 0.100992 },
        { Feature: "MntMeatProducts", Importance: 0.100206 },
        { Feature: "MntGoldProds", Importance: 0.079293 }
      ]
    }
  };
  
  res.json(analytics);
});

// Get top potential customers
app.get('/api/potential-customers', (req, res) => {
  const options = {
    mode: 'text',
    pythonPath: '/Users/trantuan/tuan-du-doan-khach-hang/venv/bin/python3',
    pythonOptions: ['-u'],
    scriptPath: path.join(__dirname, '../../analytics'),
  };

  PythonShell.run('predict_all.py', options, (err, results) => {
    if (err) {
      console.error('Error getting potential customers:', err);
      res.status(500).json({ error: 'Error getting potential customers', details: err.message });
      return;
    }

    try {
      const potentialCustomers = JSON.parse(results[0]);
      res.json(potentialCustomers);
    } catch (error) {
      console.error('Error parsing potential customers result:', error);
      res.status(500).json({ error: 'Error parsing potential customers result', details: error.message });
    }
  });
});

// Health check endpoint
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok' });
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ error: 'Something broke!', details: err.message });
});

// Handle 404
app.use((req, res) => {
  res.status(404).json({ error: 'Route not found' });
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
}); 