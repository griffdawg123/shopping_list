# Woolworths API Research

Woolworths uses an internal REST API which is a `POST` request to `https://www.woolworths.com.au/apis/ui/Search/products`.

## Endpoints

- **Search:** `https://www.woolworths.com.au/apis/ui/Search/products` (POST)
- **Product Details:** `https://www.woolworths.com.au/apis/ui/product/detail/{stockcode}` (GET)

## Search Payload

```json
{
  "SearchTerm": "milk",
  "PageSize": 36,
  "PageNumber": 1,
  "SortType": "TraderRelevance",
  "Location": "/shop/search/products?searchTerm=milk"
}
```

## Response Structure

The response returns a JSON object where the product results are in:
`Products`

Each product object contains:
- `Name`: Product name
- `DisplayName`: Displayed product name (includes brand/size)
- `Price`: Current price
- `CupString`: Unit price (e.g., "$1.55 / 1L")

## Notes
- User-Agent header is mandatory.
- Session cookies (`bm_sz`, `_abck`) may be required for some requests, but basic search often works with just a User-Agent.
- Regional pricing depends on the store ID associated with the session.
