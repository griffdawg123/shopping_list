#!/usr/bin/env python3
import sys
import requests
import json

SEARCH_URL = "https://www.woolworths.com.au/apis/ui/Search/products"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"

def search_products(query):
    payload = {
        "SearchTerm": query,
        "PageSize": 36,
        "PageNumber": 1,
        "SortType": "TraderRelevance",
        "Location": f"/shop/search/products?searchTerm={query}"
    }
    headers = {
        "User-Agent": USER_AGENT,
        "Content-Type": "application/json"
    }
    try:
        # First, hit the home page to get some base cookies
        session = requests.Session()
        session.get("https://www.woolworths.com.au/", headers={"User-Agent": USER_AGENT})
        # Set a default Sydney CBD store ID
        session.cookies.set("WOL-StoreId", "1265", domain=".woolworths.com.au")
        
        response = session.post(SEARCH_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        results = data.get("Products", [])
        if results and isinstance(results[0], dict) and "Products" in results[0]:
            # Handle case where results are nested in the first element
            results = results[0].get("Products", [])
        return results
    except Exception as e:
        print(f"Error searching Woolworths products: {e}")
        sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("Usage: ./woolworths.py <product_query>")
        sys.exit(1)

    query = sys.argv[1]
    print(f"Searching Woolworths for '{query}'...")
    results = search_products(query)

    if not results:
        print("No products found.")
        return

    print(f"{'Name':<50} | {'Price':<10} | {'Unit Price'}")
    print("-" * 80)
    for product in results:
        display_name = product.get("DisplayName", "N/A")
        price = product.get("Price", "N/A")
        unit_price = product.get("CupString", "N/A")
        print(f"{display_name:<50} | ${price:<9} | {unit_price}")

if __name__ == "__main__":
    main()
