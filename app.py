from flask import Flask, jsonify

from data.inventory import inventory

app = Flask(__name__)


@app.route("/inventory", methods=["GET"])
def get_inventory():
    return jsonify(inventory)


if __name__ == "__main__":
    app.run(debug=True)
