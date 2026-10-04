from unittest.mock import Mock, patch

import cli


def test_get_inventory():
    fake_response = Mock()
    fake_response.json.return_value = [
        {
            "id": 1,
            "name": "Coca Cola",
            "category": "Beverages",
            "barcode": "5449000000996",
            "quantity": 20,
            "price": 150
        }
    ]
    fake_response.raise_for_status.return_value = None

    with patch(
        "cli.requests.get",
        return_value=fake_response
    ):
        result = cli.get_inventory()

    assert len(result) == 1
    assert result[0]["name"] == "Coca Cola"


def test_create_inventory_item():
    fake_response = Mock()
    fake_response.status_code = 201
    fake_response.json.return_value = {
        "id": 3,
        "name": "Pepsi",
        "category": "Beverages",
        "barcode": "123456789",
        "quantity": 15,
        "price": 100
    }

    item = {
        "name": "Pepsi",
        "category": "Beverages",
        "barcode": "123456789",
        "quantity": 15,
        "price": 100
    }

    with patch(
        "cli.requests.post",
        return_value=fake_response
    ):
        response = cli.create_inventory_item(item)

    assert response.status_code == 201
    assert response.json()["name"] == "Pepsi"


def test_update_inventory_item():
    fake_response = Mock()
    fake_response.status_code = 200
    fake_response.json.return_value = {
        "id": 1,
        "name": "Coca Cola",
        "quantity": 50
    }

    with patch(
        "cli.requests.patch",
        return_value=fake_response
    ):
        response = cli.update_inventory_item(
            1,
            {"quantity": 50}
        )

    assert response.status_code == 200
    assert response.json()["quantity"] == 50


def test_delete_inventory_item():
    fake_response = Mock()
    fake_response.status_code = 200
    fake_response.json.return_value = {
        "message": "Inventory item deleted successfully"
    }

    with patch(
        "cli.requests.delete",
        return_value=fake_response
    ):
        response = cli.delete_inventory_item(1)

    assert response.status_code == 200
    
def test_search_external_products(capsys):
    fake_response = Mock()
    fake_response.status_code = 200
    fake_response.json.return_value = [
        {
            "code": "3017624010701",
            "product_name": "Nutella",
            "brands": "Ferrero"
        }
    ]

    with patch(
        "cli.input",
        return_value="nutella"
    ), patch(
        "cli.requests.get",
        return_value=fake_response
    ):
        cli.search_external_products()

    output = capsys.readouterr().out

    assert "Nutella" in output
    assert "Ferrero" in output
    
def test_import_external_product(capsys):
    fake_response = Mock()
    fake_response.status_code = 201
    fake_response.json.return_value = {
        "message": "Product imported successfully",
        "item": {
            "id": 3,
            "name": "Nutella",
            "barcode": "3017624010701"
        }
    }

    with patch(
        "cli.input",
        return_value="3017624010701"
    ), patch(
        "cli.requests.post",
        return_value=fake_response
    ):
        cli.import_external_product()

    output = capsys.readouterr().out

    assert "Product imported successfully" in output
