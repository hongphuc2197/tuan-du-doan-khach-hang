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

// Disable caching for API responses (for development)
app.use((req, res, next) => {
  res.set('Cache-Control', 'no-store, no-cache, must-revalidate, private');
  res.set('Pragma', 'no-cache');
  res.set('Expires', '0');
  next();
});

// Serve static files (images)
app.use('/images', express.static(__dirname));

// Root path
app.get('/', (req, res) => {
  res.json({ message: 'Welcome to Customer Prediction API' });
});

// Test route
app.get('/api/test', (req, res) => {
  res.json({ message: 'Test route working' });
});

// Get customers list from JSON (or CSV as fallback)
app.get('/api/customers', (req, res) => {
  try {
    const jsonPath = path.join(__dirname, 'all_customers.json');
    if (fs.existsSync(jsonPath)) {
      const data = JSON.parse(fs.readFileSync(jsonPath, 'utf8'));
      res.json(data);
      return;
    }
    
    // Fallback to CSV if JSON doesn't exist
    const results = [];
    const csvPath = path.join(__dirname, '../../result.csv');
    
    if (!fs.existsSync(csvPath)) {
      res.status(404).json({ error: 'Customer data not found' });
      return;
    }
    
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
  } catch (error) {
    console.error('Error reading customer data:', error);
    res.status(500).json({ error: 'Error reading customer data', details: error.message });
  }
});

// Predict customer endpoint
app.post('/api/predict', (req, res) => {
  const options = {
    mode: 'text',
    pythonPath: '/Users/trantuan/tuan-du-doan-khach-hang/venv/bin/python3',
    pythonOptions: ['-u'],
    scriptPath: path.join(__dirname, '../analytics'),
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

// Analytics endpoint
app.get('/api/analytics', (req, res) => {
  try {
    const jsonPath = path.join(__dirname, 'analytics_data.json');
    if (fs.existsSync(jsonPath)) {
      const data = JSON.parse(fs.readFileSync(jsonPath, 'utf8'));
      res.json(data);
    } else {
      // Fallback to Python script if JSON doesn't exist
      const options = {
        mode: 'text',
        pythonPath: '/Users/trantuan/tuan-du-doan-khach-hang/venv/bin/python3',
        pythonOptions: ['-u'],
        scriptPath: path.join(__dirname, '../analytics'),
      };

      PythonShell.run('analyze.py', options, (err, results) => {
        if (err) {
          console.error('Error running analytics:', err);
          res.status(500).json({ error: 'Error running analytics', details: err.message });
          return;
        }

        console.log('PythonShell results:', results);

        try {
          const analytics = JSON.parse(results[0]);
          res.json(analytics);
        } catch (error) {
          console.error('Error parsing analytics result:', error);
          res.status(500).json({ error: 'Error parsing analytics result', details: error.message });
        }
      });
    }
  } catch (error) {
    console.error('Error reading analytics data:', error);
    res.status(500).json({ error: 'Error reading analytics data', details: error.message });
  }
});

// Get top potential customers
app.get('/api/potential-customers', (req, res) => {
  try {
    const jsonPath = path.join(__dirname, 'potential_customers.json');
    if (fs.existsSync(jsonPath)) {
      const data = JSON.parse(fs.readFileSync(jsonPath, 'utf8'));
      res.json(data);
    } else {
      // Fallback to Python script if JSON doesn't exist
      const options = {
        mode: 'text',
        pythonPath: '/Users/trantuan/tuan-du-doan-khach-hang/venv/bin/python3',
        pythonOptions: ['-u'],
        scriptPath: path.join(__dirname, '../../analytics'),
      };

      PythonShell.run('generate_potential_customers_data.py', options, (err, results) => {
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
    }
  } catch (error) {
    console.error('Error reading potential customers:', error);
    res.status(500).json({ error: 'Error reading potential customers', details: error.message });
  }
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