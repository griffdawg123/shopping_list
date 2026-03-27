#!/usr/bin/env python3
import sys
import requests

BASE_URL = "https://apigw.coles.com.au/digital/colesappbff"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"


def search_products(query, store_id="2001", limit="20", start="0"):
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
        "Ocp-Apim-Subscription-Key": "",
    }
    params = {
        "searchTerm": query,
        "storeId": store_id,
        "start": start,
        "limit": limit,
    }
    try:
        response = requests.get(
            f"{BASE_URL}/v2/products/search", headers=headers, params=params
        )
        response.raise_for_status()
        data = response.json()
        return data.get("products", [])
    except Exception as e:
        print(f"Error searching Coles products: {e}")
        sys.exit(1)


def main():
    if len(sys.argv) < 2:
        print("Usage: ./coles_api.py <product_query>")
        sys.exit(1)

    query = sys.argv[1]
    print(f"Searching Coles for '{query}'...")
    results = search_products(query)

    if not results:
        print("No products found.")
        return

    print(f"{'Name':<50} | {'Price':<10} | {'Unit Price':<15} | {'Sale'}")
    print("-" * 90)
    for product in results:
        name = product.get("name", "N/A")
        brand = product.get("brand", "")
        full_name = f"{brand} {name}".strip()

        pricing = product.get("pricing") or {}
        price = pricing.get("now", pricing.get("cupPrice", "N/A"))
        unit_price = pricing.get("comparable", pricing.get("cupString", "N/A"))

        is_on_sale = pricing.get("promotionType") in ["SPECIAL", "DOWNDOWN"] or (
            pricing.get("was", 0) > 0
        )
        sale_star = "*" if is_on_sale else ""

        print(f"{full_name:<50} | ${price:<9} | {unit_price:<15} | {sale_star}")


if __name__ == "__main__":
    main()
