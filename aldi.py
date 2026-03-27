#!/usr/bin/env python3
import sys
import requests
import re

SEARCH_URL = "https://www.aldi.com.au/en/search-results/"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"

def search_products(query):
    params = {"q": query}
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8"
    }
    try:
        # Aldi is very restrictive, we'll try to fetch the search results page
        # Note: This might return empty if they detect automation or if no specials match
        response = requests.get(SEARCH_URL, params=params, headers=headers)
        response.raise_for_status()
        
        # We'll use regex to extract some basic product info from the HTML
        # This is a very basic fallback since they don't have a clean JSON API for search
        content = response.text
        
        # Pattern for product names and prices (simplified for demonstration)
        # Looking for something like "Basil Pesto 190g" and "$1.89"
        # From earlier findings, they use classes like box--description--header and box--price--integer
        products = []
        
        # Let's try to extract data from the __NUXT_DATA__ if it exists, otherwise use regex on HTML
        # Finding data like: {"sku":"...","name":"Basil Pesto 190g",...,"price":{"amount":189,"amountRelevantDisplay":"$1.89"}}
        
        # For simplicity in this CLI tool, we'll look for name and price in the text
        # This is a heuristic approach.
        matches = re.findall(r'"name":"([^"]+)","brandName":"[^"]*","urlSlugText":"[^"]*","urlSlugTextAlternatives":\[\],"ageRestriction":null,"alcohol":null,"discontinued":false,"discontinuedNote":null,"notForSale":false,"notForSaleReason":null,"quantityMin":1,"quantityMax":99,"quantityInterval":1,"quantityDefault":1,"quantityUnit":"[^"]*","weightType":"[^"]*","sellingSize":"[^"]*","energyClass":null,"onSaleDateDisplay":null,"isAbstract":false,"abstractSku":"[^"]*","price":{"amount":(\d+),"amountRelevant":\d+,"amountRelevantDisplay":"([^"]+)"', content)
        
        for name, amount, display_price in matches:
            if query.lower() in name.lower():
                products.append({
                    "name": name,
                    "price": display_price,
                    "unit_price": "N/A" # Unit price extraction is more complex
                })
        
        return products
    except Exception as e:
        print(f"Error searching Aldi products: {e}")
        return []

def main():
    if len(sys.argv) < 2:
        print("Usage: ./aldi.py <product_query>")
        sys.exit(1)

    query = sys.argv[1]
    print(f"Searching Aldi (Limited to Specials/Super Savers) for '{query}'...")
    results = search_products(query)

    if not results:
        print("No products found in the current online specials.")
        print("Note: Aldi Australia's website does not list their full everyday grocery range.")
        return

    print(f"{'Name':<50} | {'Price':<10}")
    print("-" * 65)
    for product in results:
        name = product.get("name", "N/A")
        price = product.get("price", "N/A")
        print(f"{name:<50} | {price}")

if __name__ == "__main__":
    main()
