# Australian Supermarket Shopping List App

A tool to help you find the cheapest groceries across Coles, Woolworths, and Aldi in Australia.

## Current Progress: Phase 1 - API Research & CLI Tools

We have successfully reverse-engineered the internal APIs for Coles and Woolworths and investigated Aldi's online presence.

### 🛠️ CLI Tools

Four Python scripts are available to search for products:

- `coles.py`: Searches Coles using their Next.js internal API.
- `woolworths.py`: Searches Woolworths using their internal REST API (defaults to Sydney CBD for pricing).
- `aldi.py`: Searches Aldi's website (limited to Special Buys and Super Savers).
- `compare.py`: Searches all three supermarkets and ranks products by price per unit.

#### Usage

```bash
./coles.py "milk"
./woolworths.py "milk"
./aldi.py "pesto"
./compare.py "milk"
```

### 📄 Documentation

Detailed research notes for each store are available in the repository:
- `COLES.md`
- `WOOLWORTHS.md`
- `ALDI.md`

## 🚀 Roadmap

1. **Design Database Schema**: Store users, lists, and cross-store product mappings.
2. **Implement Backend Service**: Price optimization engine and list management API.
3. **Store Location & Aisle Mapping**: Logic for "home shop" selection and localized sorting.
4. **Develop Web & Mobile Apps**: Modern interfaces for list creation and in-store shopping.

## 🤝 Contributing

This project uses **beads** for issue tracking.
Run `bd ready` to see available tasks.
