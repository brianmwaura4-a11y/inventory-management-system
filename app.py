from flask import Flask, jsonify, request

from external_api import get_product_by_barcode, search_products

from data.inventory import inventory

app = Flask(__name__)

#get all
@app.route("/inventory", methods=["GET"])
def get_inventory():
    return jsonify(inventory)

#get by id
@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_inventory_item(item_id):
    for item in inventory:
        if item["id"] == item_id:
            return jsonify(item)

    return jsonify({"error": "Inventory item not found"}), 404

#search helper route
@app.route("/inventory/search", methods=["GET"])
def search_inventory():
    name = request.args.get("name", "").strip().lower()

    if not name:
        return jsonify({
            "error": "Search name is required"
        }), 400

    results = [
        item for item in inventory
        if name in item["name"].lower()
    ]

    return jsonify(results), 200

#post route
@app.route("/inventory", methods=["POST"])
def create_inventory_item():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    required_fields = [
        "name",
        "category",
        "barcode",
        "quantity",
        "price"
    ]

    for field in required_fields:
        if field not in data:
            return jsonify({
                "error": f"Missing required field: {field}"
            }), 400

    for item in inventory:
        if item["barcode"] == data["barcode"]:
            return jsonify({
                "error": "An item with this barcode already exists"
            }), 409

    if not isinstance(data["quantity"], int) or data["quantity"] < 0:
        return jsonify({
            "error": "Quantity must be a non-negative integer"
        }), 400

    if not isinstance(data["price"], (int, float)) or data["price"] < 0:
        return jsonify({
            "error": "Price must be a non-negative number"
        }), 400

    new_id = max(item["id"] for item in inventory) + 1

    new_item = {
        "id": new_id,
        "name": data["name"],
        "category": data["category"],
        "barcode": data["barcode"],
        "quantity": data["quantity"],
        "price": data["price"]
    }

    inventory.append(new_item)

    return jsonify(new_item), 201

#patch route
@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_inventory_item(item_id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    item = None

    for inventory_item in inventory:
        if inventory_item["id"] == item_id:
            item = inventory_item
            break

    if item is None:
        return jsonify({"error": "Inventory item not found"}), 404

    allowed_fields = [
        "name",
        "category",
        "barcode",
        "quantity",
        "price"
    ]

    for field in data:
        if field not in allowed_fields:
            return jsonify({
                "error": f"Invalid field: {field}"
            }), 400

    if "quantity" in data:
        if not isinstance(data["quantity"], int) or data["quantity"] < 0:
            return jsonify({
                "error": "Quantity must be a non-negative integer"
            }), 400

    if "price" in data:
        if not isinstance(data["price"], (int, float)) or data["price"] < 0:
            return jsonify({
                "error": "Price must be a non-negative number"
            }), 400

    if "barcode" in data:
        for other_item in inventory:
            if (
                other_item["id"] != item_id
                and other_item["barcode"] == data["barcode"]
            ):
                return jsonify({
                    "error": "An item with this barcode already exists"
                }), 409

    for field in data:
        item[field] = data[field]

    return jsonify(item), 200

#delete route
@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_inventory_item(item_id):
    for item in inventory:
        if item["id"] == item_id:
            inventory.remove(item)

            return jsonify({
                "message": "Inventory item deleted successfully"
            }), 200

    return jsonify({
        "error": "Inventory item not found"
    }), 404

@app.route("/products/barcode/<barcode>", methods=["GET"])
def get_external_product(barcode):
    try:
        product = get_product_by_barcode(barcode)

        if product is None:
            return jsonify({
                "error": "Product not found on OpenFoodFacts"
            }), 404

        return jsonify(product), 200

    except Exception as error:
        return jsonify({
            "error": f"External API request failed: {str(error)}"
        }), 502

@app.route("/products/import", methods=["POST"])
def import_product():
    data = request.get_json()

    if not data or "barcode" not in data:
        return jsonify({
            "error": "Barcode is required"
        }), 400

    barcode = data["barcode"]

    for item in inventory:
        if item["barcode"] == barcode:
            return jsonify({
                "error": "An item with this barcode already exists"
            }), 409

    try:
        product = get_product_by_barcode(barcode)

        if product is None:
            return jsonify({
                "error": "Product not found on OpenFoodFacts"
            }), 404

    except Exception as error:
        return jsonify({
            "error": f"External API request failed: {str(error)}"
        }), 502

    product_name = product.get("product_name")

    if not product_name:
        product_name = "Unknown Product"

    brands = product.get("brands", "")
    categories = product.get("categories", "")

    category = categories.split(",")[0].strip()

    if not category:
        category = "Uncategorized"

    new_id = max(
        (item["id"] for item in inventory),
        default=0
    ) + 1

    new_item = {
        "id": new_id,
        "name": product_name,
        "category": category,
        "barcode": barcode,
        "quantity": 0,
        "price": 0,
        "brand": brands
    }

    inventory.append(new_item)

    return jsonify({
        "message": "Product imported successfully",
        "item": new_item
    }), 201
    
@app.route("/products/search", methods=["GET"])
def search_external_products():
    name = request.args.get("name", "").strip()

    if not name:
        return jsonify({
            "error": "Product name is required"
        }), 400

    try:
        products = search_products(name)

        return jsonify(products), 200

    except Exception as error:
        return jsonify({
            "error": f"External API request failed: {str(error)}"
        }), 502

if __name__ == "__main__":
    app.run(debug=True)
