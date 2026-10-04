import requests


BASE_URL = "https://world.openfoodfacts.org/api/v2"

HEADERS = {
    "User-Agent": "InventoryManagementSystem/1.0 (student-project)"
}


def get_product_by_barcode(barcode):
    url = f"{BASE_URL}/product/{barcode}"

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    if data.get("status") != 1:
        return None

    return data["product"]


def search_products(name):
    url = f"{BASE_URL}/search"

    params = {
        "search_terms": name,
        "fields": "code,product_name,brands,categories",
        "page_size": 10
    }

    response = requests.get(
        url,
        headers=HEADERS,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    return data.get("products", [])
