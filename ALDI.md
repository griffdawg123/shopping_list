# Aldi Price Strategy

**Status: Pivoted from API scraping to user-entered prices**

## Why User-Entered Prices?

Aldi will tend to be cheaper than Coles and Woolworths for most items. Rather than spending effort scraping incomplete Aldi data, we flip the model:

1. When shopping at Aldi, users enter prices they find
2. These prices are stored and used as the "best price" baseline
3. Before shopping, users check if Aldi has the item cheaper than both big supermarkets
4. If Aldi doesn't have it or it's more expensive, they shop at Coles/Woolworths

This approach:
- Is more reliable (Aldi's online presence is limited)
- Reflects reality (Aldi IS typically cheaper)
- Saves time (check Aldi first, then fill gaps at big supermarkets)

## Data Model

User-entered prices will include:
- Product name (or scanned barcode)
- Price
- Unit price (if available)
- Date entered
- Optional: store location

## Future Enhancements

- Barcode scanning for quick entry
- Receipt photo parsing (OCR)
- Crowd-sourced price database (community sharing)
