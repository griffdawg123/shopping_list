#!/usr/bin/env python3
import sys
import requests

BASE_URL = "https://prod.mobile-api.woolworths.com.au"
API_KEY = "KaGOqzzJ3ZTjswc62prswRLXCqJ4oepSqtI2P8iM"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"


def search_products(query, store_id="1265"):
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
        "X-Api-Key": API_KEY,
        "Content-Type": "application/json",
    }
    payload = {
        "searchTerm": query,
        "pageSize": 36,
        "pageNumber": 1,
        "storeId": store_id,
    }
    endpoints = [
        "/wow/v2/search",
        "/wow/v1/search",
        "/v2/search",
        "/search",
    ]
    for endpoint in endpoints:
        try:
            response = requests.post(
                f"{BASE_URL}{endpoint}", headers=headers, json=payload, timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                return data.get("products", data.get("results", []))
            elif response.status_code == 404:
                continue
            else:
                print(
                    f"Endpoint {endpoint} returned {response.status_code}: {response.text[:200]}"
                )
        except Exception as e:
            print(f"Error trying {endpoint}: {e}")
            continue

    print("No working search endpoint found")
    sys.exit(1)


def main():
    if len(sys.argv) < 2:
        print("Usage: ./woolworths_api.py <product_query>")
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
        display_name = product.get("displayName", product.get("name", "N/A"))
        price = product.get("price", product.get("now", "N/A"))
        unit_price = product.get("cupString", product.get("unitPrice", "N/A"))
        print(f"{display_name:<50} | ${price:<9} | {unit_price}")


if __name__ == "__main__":
    main()
