import copy

import pytest

from app import app
from data.inventory import inventory


@pytest.fixture(autouse=True)
def reset_inventory():
    original_inventory = copy.deepcopy(inventory)

    yield

    inventory.clear()
    inventory.extend(original_inventory)


def test_get_inventory():
    client = app.test_client()

    response = client.get("/inventory")

    assert response.status_code == 200
    assert len(response.json) == 2

def test_get_inventory_item():
    client = app.test_client()

    response = client.get("/inventory/1")

    assert response.status_code == 200
    assert response.json["name"] == "Coca Cola"

def test_get_inventory_item_not_found():
    client = app.test_client()

    response = client.get("/inventory/22")

    assert response.status_code == 404
    assert response.json["error"] == "Inventory item not found"

def test_create_inventory_item():
    client = app.test_client()

    new_item = {
        "name": "Pepsi",
        "category": "Beverages",
        "barcode": "123456789",
        "quantity": 15,
        "price": 100
    }

    response = client.post("/inventory", json=new_item)

    assert response.status_code == 201
    assert response.json["name"] == "Pepsi"
    assert response.json["quantity"] == 15

def test_create_inventory_item_missing_field():
    client = app.test_client()

    new_item = {
        "name": "Pepsi",
        "price": 100
    }

    response = client.post("/inventory", json=new_item)

    assert response.status_code == 400
    assert "Missing required field" in response.json["error"]

def test_create_inventory_item_duplicate_barcode():
    client = app.test_client()

    new_item = {
        "name": "Another Coca Cola",
        "category": "Beverages",
        "barcode": "5449000000996",
        "quantity": 10,
        "price": 100
    }

    response = client.post("/inventory", json=new_item)

    assert response.status_code == 409

def test_create_inventory_item_invalid_quantity():
    client = app.test_client()

    new_item = {
        "name": "Pepsi",
        "category": "Beverages",
        "barcode": "987654321",
        "quantity": -5,
        "price": 100
    }

    response = client.post("/inventory", json=new_item)

    assert response.status_code == 400
    
def test_update_inventory_item():
    client = app.test_client()

    response = client.patch(
        "/inventory/1",
        json={"quantity": 50}
    )

    assert response.status_code == 200
    assert response.json["quantity"] == 50
    assert response.json["name"] == "Coca Cola"
    
def test_update_multiple_inventory_fields():
    client = app.test_client()

    response = client.patch(
        "/inventory/1",
        json={
            "quantity": 30,
            "price": 175
        }
    )

    assert response.status_code == 200
    assert response.json["quantity"] == 30
    assert response.json["price"] == 175
    
def test_update_inventory_item_not_found():
    client = app.test_client()

    response = client.patch(
        "/inventory/999",
        json={"quantity": 50}
    )

    assert response.status_code == 404
    assert response.json["error"] == "Inventory item not found"
    
def test_update_inventory_item_invalid_quantity():
    client = app.test_client()

    response = client.patch(
        "/inventory/1",
        json={"quantity": -10}
    )

    assert response.status_code == 400
    assert response.json["error"] == (
        "Quantity must be a non-negative integer"
    )
    
def test_update_inventory_item_invalid_field():
    client = app.test_client()

    response = client.patch(
        "/inventory/1",
        json={"customer_password": "12345"}
    )

    assert response.status_code == 400
    assert "Invalid field" in response.json["error"]
    
def test_delete_inventory_item():
    client = app.test_client()

    response = client.delete("/inventory/2")

    assert response.status_code == 200
    assert response.json["message"] == (
        "Inventory item deleted successfully"
    )
    
def test_deleted_inventory_item_is_not_found():
    client = app.test_client()

    client.delete("/inventory/2")

    response = client.get("/inventory/2")

    assert response.status_code == 404
    
def test_delete_inventory_item_not_found():
    client = app.test_client()

    response = client.delete("/inventory/22")

    assert response.status_code == 404
    assert response.json["error"] == "Inventory item not found"

def test_search_inventory():
    client = app.test_client()

    response = client.get("/inventory/search?name=coca")

    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]["name"] == "Coca Cola"
    
def test_search_inventory_without_name():
    client = app.test_client()

    response = client.get("/inventory/search")

    assert response.status_code == 400
    assert response.json["error"] == "Search name is required"
