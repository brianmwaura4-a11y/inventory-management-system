from flask import Flask, jsonify

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

if __name__ == "__main__":
    app.run(debug=True)
