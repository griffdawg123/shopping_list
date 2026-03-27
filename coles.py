#!/usr/bin/env python3
import sys
import requests
import re
import json

BASE_URL = "https://www.coles.com.au"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"

HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Referer": "https://www.google.com/",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

def get_build_id():
    try:
        session = requests.Session()
        response = session.get(BASE_URL, headers=HEADERS)
        response.raise_for_status()
        match = re.search(r'"buildId":"([^"]+)"', response.text)
        if match:
            return match.group(1)
        else:
            # Fallback to curl if requests is blocked
            import subprocess
            cmd = f'curl -s -H "User-Agent: {USER_AGENT}" {BASE_URL} | grep -o \'"buildId":"[^"]*"\' | cut -d\'"\' -f4'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.stdout.strip():
                return result.stdout.strip()
            print("Error: Could not find buildId")
            sys.exit(1)
    except Exception as e:
        print(f"Error fetching Coles home page: {e}")
        sys.exit(1)

def search_products(query, build_id):
    search_url = f"{BASE_URL}/_next/data/{build_id}/en/search/products.json?q={query}"
    try:
        response = requests.get(search_url, headers=HEADERS)
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

    print(f"{'Name':<50} | {'Price':<10} | {'Unit Price':<15} | {'Sale'}")
    print("-" * 90)
    for product in results:
        # Only process items that are actually products
        if product.get("_type") != "PRODUCT":
            continue
            
        name = product.get("name", "N/A")
        brand = product.get("brand", "")
        full_name = f"{brand} {name}".strip()
        pricing = product.get("pricing") or {}
        price = pricing.get("now", "N/A")
        unit_price = pricing.get("comparable", "N/A")
        
        # Check if on sale
        # Coles products on sale usually have a 'was' price or a promotion object
        promotion = pricing.get("promotionType")
        is_on_sale = promotion in ["SPECIAL", "DOWNDOWN"] or (pricing.get("was", 0) > 0)
        sale_star = "*" if is_on_sale else ""
        
        print(f"{full_name:<50} | ${price:<9} | {unit_price:<15} | {sale_star}")

if __name__ == "__main__":
    main()
