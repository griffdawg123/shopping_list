# Australian Supermarket Shopping List App

A tool to help you find the cheapest groceries across Coles, Woolworths, and Aldi in Australia.

## Quick Start

### Web App (Recommended)

```bash
cd shopping-web
npm install
npm start          # Terminal 1: React app on http://localhost:3000
node server.js     # Terminal 2: Backend API
```

Open http://localhost:3000 in your browser.

### CLI Tools

```bash
./coles.py "milk"       # Search Coles
./woolworths.py "milk"  # Search Woolworths
./compare.py "milk"     # Compare both (ranked by unit price)
```

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   React Web     │────▶│   Express.js    │────▶│   Python CLI    │
│   (localhost)   │     │   (port 3000)    │     │   Scripts       │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                        │
                                                        ▼
                                                ┌─────────────────┐
                                                │   Coles/WW      │
                                                │   Scrapers      │
                                                └─────────────────┘
```

## Project Structure

```
shopping/
├── shopping-web/           # React web app (recommended)
│   ├── src/
│   │   ├── components/    # UI components
│   │   ├── services/      # API client
│   │   └── types/         # TypeScript types
│   └── server.js          # Express backend
├── ShoppingApp/           # React Native mobile app (experimental)
├── ShoppingApp/           # React Native mobile app (experimental)
├── au-supermarket-apis/   # API specifications
├── coles_api.py          # Coles API script (requires key)
├── woolworths_api.py      # Woolworths API script (requires key)
├── compare.py             # Price comparison script
├── coles.py               # Coles scraper
├── woolworths.py          # Woolworths scraper
└── aldi.py               # Aldi scraper (limited)
```

## Aldi Strategy

**User-entered prices** - Aldi has no public API. Instead, users enter prices they find while shopping at Aldi. See [ALDI.md](ALDI.md) for details.

## Documentation

- [COLES.md](COLES.md) - Coles API research
- [WOOLWORTHS.md](WOOLWORTHS.md) - Woolworths API research
- [ALDI.md](ALDI.md) - Aldi strategy (user-entered prices)
- [au-supermarket-apis/README.md](au-supermarket-apis/README.md) - API specs

## Roadmap

- [x] Coles/Woolworths price comparison
- [x] Web app interface
- [ ] User-entered Aldi price storage
- [ ] Product barcode scanning
- [ ] Cross-store product matching
- [ ] Price history tracking
