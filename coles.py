#!/usr/bin/env python3
import sys
import requests
import re
import json

BASE_URL = "https://www.coles.com.au"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"

def get_build_id():
    try:
        response = requests.get(BASE_URL, headers={"User-Agent": USER_AGENT})
        response.raise_for_status()
        match = re.search(r'"buildId":"([^"]+)"', response.text)
        if match:
            return match.group(1)
        else:
            print("Error: Could not find buildId")
            sys.exit(1)
    except Exception as e:
        print(f"Error fetching Coles home page: {e}")
        sys.exit(1)

def search_products(query, build_id):
    search_url = f"{BASE_URL}/_next/data/{build_id}/en/search/products.json?q={query}"
    try:
        response = requests.get(search_url, headers={"User-Agent": USER_AGENT})
        response.raise_for_status()
        data = response.json()
        results = data.get("pageProps", {}).get("searchResults", {}).get("results", [])
        return results
    except Exception as e:
        print(f"Error searching Coles products: {e}")
        sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("Usage: ./coles.py <product_query>")
        sys.exit(1)

    query = sys.argv[1]
    print(f"Searching Coles for '{query}'...")
    build_id = get_build_id()
    results = search_products(query, build_id)

    if not results:
        print("No products found.")
        return

    print(f"{'Name':<50} | {'Price':<10} | {'Unit Price'}")
    print("-" * 80)
    for product in results:
        name = product.get("name", "N/A")
        brand = product.get("brand", "")
        full_name = f"{brand} {name}".strip()
        price = product.get("pricing", {}).get("now", "N/A")
        unit_price = product.get("pricing", {}).get("comparable", "N/A")
        print(f"{full_name:<50} | ${price:<9} | {unit_price}")

if __name__ == "__main__":
    main()
