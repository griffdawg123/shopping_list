# Coles API Research

Coles uses a Next.js-powered website which fetches data from internal JSON endpoints. These endpoints require a dynamic `buildId` which can be found in the page source.

## Endpoints

- **Search:** `https://www.coles.com.au/_next/data/{buildId}/en/search/products.json?q={query}`
- **Product Details:** `https://www.coles.com.au/_next/data/{buildId}/en/product/{slug}.json`

## Finding the buildId

The `buildId` is located within the `__NEXT_DATA__` script tag on any page (e.g., the home page).
Example extraction:
```bash
curl -s https://www.coles.com.au/ | grep -oP '"buildId":"\K[^"]+'
```

## Response Structure

The search endpoint returns a JSON object. The product results are found under:
`pageProps.searchResults.results`

Each product object contains:
- `name`: Product name
- `brand`: Brand name
- `pricing.now`: Current price
- `pricing.comparable`: Unit price (e.g., "$1.55 / 1L")

## Notes
- User-Agent header is mandatory.
- Regional pricing depends on store location, which might require specific cookies or headers.
