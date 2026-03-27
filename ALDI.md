# Aldi API Research

Aldi Australia does not have a comprehensive public search API for all groceries. Its website primarily focuses on **Special Buys** and **Super Savers**.

## Endpoints

- **Special Buys / Super Savers:** `https://www.aldi.com.au/products`
- **Search (Limited):** `https://www.aldi.com.au/en/search-results/?q={query}`

## Reverse Engineering Insights

Aldi uses a Nuxt.js-powered frontend. The product data for the current page is often embedded in the `__NUXT_DATA__` script tag or similar JSON structures within the HTML.

### Alternative: DoorDash API
A more comprehensive list of Aldi's everyday range can be accessed via the **DoorDash API**, as Aldi uses DoorDash for its delivery service.
- **DoorDash Store ID:** Required to fetch the menu.
- **Endpoint:** `https://www.doordash.com/api/v2/store/{store_id}/menu/`

## Response Structure (Web Scrape)

When scraping the website, look for these fields in the embedded JSON:
- `name`: Product name
- `price.amountRelevantDisplay`: Current price
- `price.comparisonDisplay`: Unit price (e.g., "$0.99 per 100 g")

## Notes
- User-Agent header is mandatory.
- Regional availability is highly relevant at Aldi.
- Full inventory is generally not available online via Aldi's official channels.
