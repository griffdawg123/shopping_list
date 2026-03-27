#!/usr/bin/env python3
import sys
import requests
import re
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor

# Reuse logic from other scripts where possible or redefine for self-containedness
COLES_BASE_URL = "https://www.coles.com.au"
WOOLIES_SEARCH_URL = "https://www.woolworths.com.au/apis/ui/Search/products"
ALDI_SEARCH_URL = "https://www.aldi.com.au/en/search-results/"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"

COMMON_HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept": "application/json, text/plain, */*",
}

def parse_unit_price(s):
    if not s or s == "N/A":
        return None, None
    
    # Matches: $1.50, 100, g/ml/kg/l/ea
    # Example: "$1.50/ 100g" or "$2.50 / 1kg" or "$0.50 per 1 ea"
    match = re.search(r'\$([\d\.]+)\s*(?:/|per)\s*([\d\.]+)?\s*(\w+)', s, re.IGNORECASE)
    if match:
        try:
            price = float(match.group(1))
            qty = float(match.group(2)) if match.group(2) else 1.0
            unit = match.group(3).lower()
            
            # Normalize to price per 100g/ml or 1ea
            if unit in ["g", "ml"]:
                return (price / qty) * 100, f"per 100{unit}"
            if unit in ["kg", "l"]:
                # 1kg = 1000g, so 100g is 0.1kg.
                # price for 1kg -> price/10 for 100g
                return (price / (qty * 10)), f"per 100{'g' if unit == 'kg' else 'ml'}"
            if unit == "ea":
                return price / qty, "per 1ea"
        except:
            pass
            
    return None, None

def search_coles(query):
    # Get buildId first (using curl fallback like in coles.py)
    cmd = f'curl -s -L -H "User-Agent: {USER_AGENT}" {COLES_BASE_URL} | grep -o \'"buildId":"[^"]*"\' | cut -d\'"\' -f4'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    build_id = result.stdout.strip()
    if not build_id:
        return []

    search_url = f"{COLES_BASE_URL}/_next/data/{build_id}/en/search/products.json?q={query}"
    try:
        response = requests.get(search_url, headers=COMMON_HEADERS)
        response.raise_for_status()
        data = response.json()
        raw_results = data.get("pageProps", {}).get("searchResults", {}).get("results", [])
        
        products = []
        for r in raw_results:
            if r.get("_type") != "PRODUCT":
                continue
            name = f"{r.get('brand', '')} {r.get('name', '')}".strip()
            pricing = r.get("pricing") or {}
            price = pricing.get("now", "N/A")
            unit_price_str = pricing.get("comparable", "N/A")
            norm_price, norm_unit = parse_unit_price(unit_price_str)
            
            products.append({
                "store": "Coles",
                "name": name,
                "price": price,
                "unit_price_str": unit_price_str,
                "norm_price": norm_price,
                "norm_unit": norm_unit,
                "on_sale": (pricing.get("promotionType") in ["SPECIAL", "DOWNDOWN"]) or (pricing.get("was", 0) > 0)
            })
        return products
    except:
        return []

def search_woolworths(query):
    payload = {
        "SearchTerm": query, "PageSize": 36, "PageNumber": 1,
        "SortType": "TraderRelevance", "Location": f"/shop/search/products?searchTerm={query}"
    }
    try:
        session = requests.Session()
        session.get("https://www.woolworths.com.au/", headers={"User-Agent": USER_AGENT})
        session.cookies.set("WOL-StoreId", "1265", domain=".woolworths.com.au")
        
        response = session.post(WOOLIES_SEARCH_URL, headers=COMMON_HEADERS, json=payload)
        response.raise_for_status()
        data = response.json()
        
        tiles = data.get("Products", [])
        raw_results = []
        for tile in tiles:
            if tile is not None and "Products" in tile and tile["Products"]:
                raw_results.extend(tile["Products"])
            
        products = []
        for r in raw_results:
            name = r.get("DisplayName", "N/A")
            price = r.get("Price", "N/A")
            unit_price_str = r.get("CupString", "N/A")
            norm_price, norm_unit = parse_unit_price(unit_price_str)
            
            # Woolworths sale check
            is_on_sale = r.get("IsSpecial", False) or r.get("IsBundle", False) or "Low Price" in (r.get("LabelHtml", "") or "")
            
            products.append({
                "store": "Woolworths",
                "name": name,
                "price": price,
                "unit_price_str": unit_price_str,
                "norm_price": norm_price,
                "norm_unit": norm_unit,
                "on_sale": is_on_sale
            })
        return products
    except:
        return []

def search_aldi(query):
    params = {"q": query}
    try:
        response = requests.get(ALDI_SEARCH_URL, params=params, headers=COMMON_HEADERS)
        response.raise_for_status()
        content = response.text
        
        # More advanced regex to find products in Nuxt data if possible
        # Look for name and price
        matches = re.findall(r'"name":"([^"]+)","brandName":"[^"]*".*?"price":{"amount":\d+,"amountRelevant":\d+,"amountRelevantDisplay":"([^"]+)".*?"comparisonDisplay":"([^"]+)"', content)
        
        products = []
        for name, display_price, unit_price_str in matches:
            if query.lower() in name.lower():
                price = display_price.replace("$", "")
                norm_price, norm_unit = parse_unit_price(unit_price_str)
                products.append({
                    "store": "Aldi",
                    "name": name,
                    "price": price,
                    "unit_price_str": unit_price_str,
                    "norm_price": norm_price,
                    "norm_unit": norm_unit,
                    "on_sale": True # Aldi search results are mostly specials
                })
        return products
    except:
        return []

def main():
    if len(sys.argv) < 2:
        print("Usage: ./compare.py <product_query>")
        sys.exit(1)

    query = sys.argv[1]
    print(f"Searching for '{query}' across supermarkets...")

    with ThreadPoolExecutor(max_workers=3) as executor:
        f_coles = executor.submit(search_coles, query)
        f_woolies = executor.submit(search_woolworths, query)
        f_aldi = executor.submit(search_aldi, query)
        
        all_products = f_coles.result() + f_woolies.result() + f_aldi.result()

    if not all_products:
        print("No products found.")
        return

    # Filter out products without unit price for ranking
    rankable = [p for p in all_products if p["norm_price"] is not None]
    # Sort by normalized price
    rankable.sort(key=lambda x: x["norm_price"])

    print(f"{'Store':<12} | {'Name':<50} | {'Price':<8} | {'Unit Price':<15} | {'Sale'}")
    print("-" * 100)
    for p in rankable:
        sale_star = "*" if p["on_sale"] else ""
        price_val = f"${p['price']}" if isinstance(p['price'], (int, float)) or (isinstance(p['price'], str) and p['price'] != "N/A") else "N/A"
        print(f"{p['store']:<12} | {p['name']:<50} | {price_val:<8} | {p['unit_price_str']:<15} | {sale_star}")

    # Show non-rankable items at the end
    non_rankable = [p for p in all_products if p["norm_price"] is None]
    if non_rankable:
        print("\nItems without comparable unit price:")
        for p in non_rankable:
            sale_star = "*" if p["on_sale"] else ""
            price_val = f"${p['price']}" if isinstance(p['price'], (int, float)) or (isinstance(p['price'], str) and p['price'] != "N/A") else "N/A"
            print(f"{p['store']:<12} | {p['name']:<50} | {price_val:<8} | {p['unit_price_str']:<15} | {sale_star}")

if __name__ == "__main__":
    main()
