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
