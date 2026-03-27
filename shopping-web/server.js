const express = require('express');
const {spawn} = require('child_process');
const path = require('path');

const app = express();
const PORT = 3000;

app.use(express.json());
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.header('Access-Control-Allow-Headers', 'Content-Type');
  next();
});

app.get('/api/compare', (req, res) => {
  const query = req.query.q;

  if (!query) {
    return res.status(400).json({error: 'Query parameter required'});
  }

  res.set('Cache-Control', 'no-store');

  const scriptPath = path.join(__dirname, '..', 'compare.py');
  const python = spawn('python3', [scriptPath, query]);

  let output = '';
  let errorOutput = '';

  python.stdout.on('data', data => {
    output += data.toString();
  });

  python.stderr.on('data', data => {
    errorOutput += data.toString();
  });

  python.on('close', code => {
    if (code !== 0) {
      console.error('Python script error:', errorOutput);
      return res.status(500).json({error: 'Script execution failed'});
    }

    const products = parseOutput(output);
    res.json({products});
  });
});

function parseOutput(output) {
  const lines = output.trim().split('\n');
  const products = [];

  for (const line of lines) {
    if (line.includes('|') && line.includes('$')) {
      const parts = line.split('|').map(p => p.trim());
      if (parts.length >= 5) {
        const supermarket = parts[0].toLowerCase().includes('coles') ? 'coles' : 'woolworths';
        const name = parts[1];
        const price = parts[2].replace('$', '');
        const unitPrice = parts[3];
        const isOnSale = parts[4] === '*';

        products.push({name, price, unitPrice, supermarket, isOnSale});
      }
    }
  }

  return products;
}

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
