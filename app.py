from flask import Flask, jsonify, request

from data.inventory import inventory

app = Flask(__name__)


@app.route("/inventory", methods=["GET"])
def get_inventory():
    return jsonify(inventory)

@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_inventory_item(item_id):
    for item in inventory:
        if item["id"] == item_id:
            return jsonify(item)

    return jsonify({"error": "Inventory item not found"}), 404

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

if __name__ == "__main__":
    app.run(debug=True)
