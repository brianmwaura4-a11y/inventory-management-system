from app import app


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