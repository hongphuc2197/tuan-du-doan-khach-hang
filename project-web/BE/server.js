// server.js (refactor)

const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const { PythonShell } = require('python-shell');
const csv = require('csv-parser');
const fs = require('fs');
const path = require('path');

const app = express();
const port = process.env.PORT || 5001;

// ===== Middleware
app.use(cors());
app.use(bodyParser.json({ limit: '2mb' })); // tăng limit nếu payload lớn

// ===== Utils
function runPy(scriptName, { args = [], timeoutMs = 15000 } = {}) {
  return new Promise((resolve, reject) => {
    const scriptPath = path.join(__dirname, '../../analytics');

    const pythonPath =
      process.env.PYTHON_PATH ||
      '/Users/trantuan/tuan-du-doan-khach-hang/venv/bin/python3'; // mặc định theo máy bạn

    const options = {
      mode: 'text',
      pythonPath,
      pythonOptions: ['-u'], // unbuffered để nhận log realtime
      scriptPath,
    };

    const fullScript = path.join(scriptPath, scriptName);
    if (!fs.existsSync(fullScript)) {
      return reject(new Error(`Script not found: ${fullScript}`));
    }

    console.log(`[runPy] Using pythonPath=${pythonPath}`);
    console.log(`[runPy] Running ${fullScript} with args=`, args);

    const pyshell = new PythonShell(scriptName, { ...options, args });
    let out = '';
    let errOut = '';

    pyshell.on('message', (msg) => {
      // STDOUT của Python
      console.log(`[py:${scriptName}:stdout] ${msg}`);
      out += msg + '\n';
    });

    pyshell.on('stderr', (s) => {
      // STDERR của Python
      console.error(`[py:${scriptName}:stderr] ${s}`);
      errOut += s + '\n';
    });

    const timer = setTimeout(() => {
      console.error(`[runPy] Timeout after ${timeoutMs}ms -> terminate ${scriptName}`);
      try {
        pyshell.terminate();
      } catch (e) {
        console.error(`[runPy] terminate error:`, e);
      }
    }, timeoutMs);

    pyshell.end((err, code, signal) => {
      clearTimeout(timer);

      console.log(`[runPy] ${scriptName} ended with code=${code} signal=${signal}`);

      if (err) {
        return reject(
          new Error(`Python error: ${err.message}\n--- STDERR ---\n${errOut}`)
        );
      }

      const raw = (out || '').trim();
      if (!raw) {
        return reject(new Error(`Python returned no output.\n--- STDERR ---\n${errOut}`));
      }

      try {
        const data = JSON.parse(raw);
        return resolve(data);
      } catch (e) {
        return reject(
          new Error(
            `JSON parse failed: ${e.message}\n--- STDOUT ---\n${raw}\n--- STDERR ---\n${errOut}`
          )
        );
      }
    });
  });
}

// ===== Root path
app.get('/', (req, res) => {
  res.json({ message: 'Welcome to Customer Prediction API' });
});

// ===== Test route
app.get('/api/test', (req, res) => {
  res.json({ message: 'Test route working' });
});

// ===== Get customers list from CSV
app.get('/api/customers', (req, res) => {
  const csvPath = path.join(__dirname, '../../result.csv');

  if (!fs.existsSync(csvPath)) {
    console.error('[CSV] File not found:', csvPath);
    return res.status(404).json({ error: 'Customer CSV not found' });
  }

  const results = [];
  fs.createReadStream(csvPath)
    .on('error', (error) => {
      console.error('Error opening CSV:', error);
      res.status(500).json({ error: 'Error opening customer data CSV' });
    })
    .pipe(csv())
    .on('data', (data) => {
      const processedData = {};
      Object.keys(data).forEach((key) => {
        if (key === 'ID') {
          processedData[key] = data[key];
        } else {
          const value = data[key] === '' ? 0 : parseFloat(data[key]);
          processedData[key] = isNaN(value) ? 0 : value;
        }
      });

      // Chuẩn hoá vài field dùng ở FE (tuỳ file CSV của bạn)
      processedData.TotalSpent =
        processedData.TotalSpending ?? processedData.TotalSpent ?? 0;
      processedData.AvgPurchaseValue = processedData.AvgPurchaseValue ?? 0;

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

// ===== Predict customer endpoint
app.post('/api/predict', async (req, res) => {
  try {
    const bodyArg = JSON.stringify(req.body || {});
    const data = await runPy('predict.py', { args: [bodyArg], timeoutMs: 30000 });
    res.json(data);
  } catch (e) {
    console.error('[API /api/predict] error:', e);
    res.status(500).json({ error: 'Error running prediction', details: String(e) });
  }
});

// ===== Analytics endpoint
app.get('/api/analytics', async (req, res) => {
  try {
    const data = await runPy('analyze.py', { timeoutMs: 30000 });
    res.json(data);
  } catch (e) {
    console.error('[API /api/analytics] error:', e);
    res.status(500).json({ error: 'Error running analytics', details: String(e) });
  }
});

// ===== Get top potential customers
app.get('/api/potential-customers', async (req, res) => {
  try {
    const data = await runPy('predict_all.py', { timeoutMs: 60000 });
    res.json(data);
  } catch (e) {
    console.error('[API /api/potential-customers] error:', e);
    res.status(500).json({ error: 'Error getting potential customers', details: String(e) });
  }
});

// ===== Health check endpoint
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok' });
});

// ===== Error handling middleware
// (Chỉ bắt lỗi sync trong middleware trước đó; lỗi async đã try/catch rồi)
app.use((err, req, res, next) => {
  console.error('[Global Error]', err.stack || err);
  res.status(500).json({ error: 'Something broke!', details: err.message || String(err) });
});

// ===== 404
app.use((req, res) => {
  res.status(404).json({ error: 'Route not found' });
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
