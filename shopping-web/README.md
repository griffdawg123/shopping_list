# Shopping Compare

A web app for comparing supermarket prices across Coles and Woolworths.

## Quick Start

```bash
cd shopping-web
npm install
npm start          # Terminal 1: React app on http://localhost:3000
node server.js     # Terminal 2: Backend on http://localhost:3000
```

Then open http://localhost:3000 in your browser.

## Features

- Search products and compare Coles vs Woolworths prices
- Shopping list with checkboxes
- Color-coded supermarket badges

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   React Web     │────▶│   Express.js    │────▶│   Python CLI    │
│   (localhost)   │     │   (port 3000)    │     │   Scripts       │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

## CLI Tools (from parent directory)

```bash
./coles.py "milk"      # Search Coles
./woolworths.py "milk" # Search Woolworths
./compare.py "milk"    # Compare both
```

## Project Structure

```
shopping/
├── shopping-web/           # React web app
│   ├── src/
│   │   ├── components/     # UI components
│   │   ├── services/       # API client
│   │   └── types/          # TypeScript types
│   └── server.js           # Express backend
├── ShoppingApp/            # React Native mobile app (experimental)
├── compare.py              # Python comparison script
└── ALDI.md                 # Aldi strategy
```
