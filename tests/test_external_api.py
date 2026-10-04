import copy
from unittest.mock import Mock, patch
import pytest
from app import app
from data.inventory import inventory
from external_api import (get_product_by_barcode, search_products)

@pytest.fixture(autouse=True)
def reset_inventory():
    original_inventory = copy.deepcopy(inventory)

    yield

    inventory.clear()
    inventory.extend(original_inventory)

def test_get_product_by_barcode():
    fake_response = Mock()

    fake_response.json.return_value = {
        "status": 1,
        "product": {
            "code": "3017624010701",
            "product_name": "Nutella",
            "brands": "Ferrero",
            "categories": "Spreads"
        }
    }

    fake_response.raise_for_status.return_value = None

    with patch(
        "external_api.requests.get",
        return_value=fake_response
    ):
        product = get_product_by_barcode("3017624010701")

    assert product["product_name"] == "Nutella"
    assert product["brands"] == "Ferrero"


def test_get_product_by_barcode_not_found():
    fake_response = Mock()

    fake_response.json.return_value = {
        "status": 0
    }

    fake_response.raise_for_status.return_value = None

    with patch(
        "external_api.requests.get",
        return_value=fake_response
    ):
        product = get_product_by_barcode("0000000000000")

    assert product is None


def test_search_products():
    fake_response = Mock()

    fake_response.json.return_value = {
        "products": [
            {
                "code": "3017624010701",
                "product_name": "Nutella",
                "brands": "Ferrero",
                "categories": "Spreads"
            }
        ]
    }

    fake_response.raise_for_status.return_value = None

    with patch(
        "external_api.requests.get",
        return_value=fake_response
    ):
        products = search_products("nutella")

    assert len(products) == 1
    assert products[0]["product_name"] == "Nutella"

def test_barcode_route():
    fake_product = {
        "code": "3017624010701",
        "product_name": "Nutella",
        "brands": "Ferrero",
        "categories": "Spreads"
    }

    with patch(
        "app.get_product_by_barcode",
        return_value=fake_product
    ):
        client = app.test_client()

        response = client.get(
            "/products/barcode/3017624010701"
        )

    assert response.status_code == 200
    assert response.json["product_name"] == "Nutella"
    
def test_barcode_route_product_not_found():
    with patch(
        "app.get_product_by_barcode",
        return_value=None
    ):
        client = app.test_client()

        response = client.get(
            "/products/barcode/0000000000000"
        )

    assert response.status_code == 404
    assert response.json["error"] == (
        "Product not found on OpenFoodFacts"
    )
    
def test_external_product_search_route():
    fake_products = [
        {
            "code": "3017624010701",
            "product_name": "Nutella",
            "brands": "Ferrero",
            "categories": "Spreads"
        }
    ]

    with patch(
        "app.search_products",
        return_value=fake_products
    ):
        client = app.test_client()

        response = client.get(
            "/products/search?name=nutella"
        )

    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]["product_name"] == "Nutella"
    
def test_external_product_search_without_name():
    client = app.test_client()

    response = client.get("/products/search")

    assert response.status_code == 400
    assert response.json["error"] == (
        "Product name is required"
    )
    
def test_import_external_product():
    fake_product = {
        "code": "3017624010701",
        "product_name": "Nutella",
        "brands": "Ferrero",
        "categories": "Spreads"
    }

    with patch(
        "app.get_product_by_barcode",
        return_value=fake_product
    ):
        client = app.test_client()

        response = client.post(
            "/products/import",
            json={
                "barcode": "3017624010701"
            }
        )

    assert response.status_code == 201
    assert response.json["message"] == (
        "Product imported successfully"
    )
    assert response.json["item"]["name"] == "Nutella"
    assert response.json["item"]["barcode"] == (
        "3017624010701"
    )
    
def test_import_external_product_duplicate():
    inventory.append({
        "id": 3,
        "name": "Nutella",
        "category": "Spreads",
        "barcode": "3017624010701",
        "quantity": 0,
        "price": 0
    })

    client = app.test_client()

    response = client.post(
        "/products/import",
        json={
            "barcode": "3017624010701"
        }
    )

    assert response.status_code == 409
    assert response.json["error"] == (
        "An item with this barcode already exists"
    )
