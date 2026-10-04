import requests
from external_api import (search_products, get_product_by_barcode)

BASE_URL = "http://127.0.0.1:5000"


def get_inventory():
    response = requests.get(f"{BASE_URL}/inventory")
    response.raise_for_status()
    return response.json()


def get_inventory_item(item_id):
    response = requests.get(f"{BASE_URL}/inventory/{item_id}")
    return response


def create_inventory_item(item):
    response = requests.post(
        f"{BASE_URL}/inventory",
        json=item
    )
    return response


def update_inventory_item(item_id, data):
    response = requests.patch(
        f"{BASE_URL}/inventory/{item_id}",
        json=data
    )
    return response


def delete_inventory_item(item_id):
    response = requests.delete(
        f"{BASE_URL}/inventory/{item_id}"
    )
    return response

def display_inventory():
    response = get_inventory()

    if not response:
        print("No inventory items found.")
        return

    print("\nInventory")
    print("-" * 60)

    for item in response:
        print(
            f"ID: {item['id']} | "
            f"Name: {item['name']} | "
            f"Category: {item['category']} | "
            f"Quantity: {item['quantity']} | "
            f"Price: {item['price']}"
        )

    print("-" * 60)
    
def show_menu():
    print("\nInventory Management System")
    print("1. View inventory")
    print("2. Get inventory item")
    print("3. Add inventory item")
    print("4. Update inventory item")
    print("5. Delete inventory item")
    print("6. Exit")
    print("7. Search OpenFoodFacts")
    print("8. Import product from OpenFoodFacts")
    
def main():
    while True:
        show_menu()

        choice = input("Choose an option: ").strip()

        if choice == "1":
            display_inventory()

        elif choice == "2":
            display_inventory_item()

        elif choice == "3":
            add_inventory_item()

        elif choice == "4":
            edit_inventory_item()

        elif choice == "5":
            remove_inventory_item()
        
        elif choice == "6":
            print("Goodbye!")
            break
        
        elif choice == "7":
            search_external_products()

        elif choice == "8":
            import_external_product()

        else:
            print("Invalid option. Please choose 1-8.")
            
def display_inventory_item():
    item_id = input("Enter item ID: ").strip()

    if not item_id.isdigit():
        print("ID must be a number.")
        return

    response = get_inventory_item(int(item_id))

    if response.status_code == 200:
        item = response.json()

        print("\nInventory Item")
        print("-" * 40)
        print(f"ID: {item['id']}")
        print(f"Name: {item['name']}")
        print(f"Category: {item['category']}")
        print(f"Barcode: {item['barcode']}")
        print(f"Quantity: {item['quantity']}")
        print(f"Price: {item['price']}")
    else:
        print(response.json().get("error", "Item not found"))

def add_inventory_item():
    name = input("Name: ").strip()
    category = input("Category: ").strip()
    barcode = input("Barcode: ").strip()
    quantity = input("Quantity: ").strip()
    price = input("Price: ").strip()

    if not quantity.isdigit():
        print("Quantity must be a non-negative integer.")
        return

    try:
        price = float(price)
    except ValueError:
        print("Price must be a number.")
        return

    item = {
        "name": name,
        "category": category,
        "barcode": barcode,
        "quantity": int(quantity),
        "price": price
    }

    response = create_inventory_item(item)

    if response.status_code == 201:
        print("\nItem added successfully.")
        print(response.json())
    else:
        print(response.json().get("error", "Failed to add item"))

def edit_inventory_item():
    item_id = input("Enter item ID: ").strip()

    if not item_id.isdigit():
        print("ID must be a number.")
        return

    print("\nLeave a field blank to keep its current value.")

    quantity = input("New quantity: ").strip()
    price = input("New price: ").strip()

    data = {}

    if quantity:
        if not quantity.isdigit():
            print("Quantity must be a non-negative integer.")
            return

        data["quantity"] = int(quantity)

    if price:
        try:
            data["price"] = float(price)
        except ValueError:
            print("Price must be a number.")
            return

    if not data:
        print("No changes provided.")
        return

    response = update_inventory_item(int(item_id), data)

    if response.status_code == 200:
        print("\nItem updated successfully.")
        print(response.json())
    else:
        print(response.json().get("error", "Failed to update item"))

def remove_inventory_item():
    item_id = input("Enter item ID: ").strip()

    if not item_id.isdigit():
        print("ID must be a number.")
        return

    response = delete_inventory_item(int(item_id))

    if response.status_code == 200:
        print("\nItem deleted successfully.")
    else:
        print(response.json().get("error", "Failed to delete item"))
        
def search_external_products():
    name = input("Enter product name: ").strip()

    if not name:
        print("Product name is required.")
        return

    response = requests.get(
        f"{BASE_URL}/products/search",
        params={"name": name}
    )

    if response.status_code != 200:
        print(response.json().get(
            "error",
            "Failed to search OpenFoodFacts"
        ))
        return

    products = response.json()

    if not products:
        print("No products found.")
        return

    print("\nOpenFoodFacts Results")
    print("-" * 60)

    for product in products:
        print(
            f"Barcode: {product.get('code', 'N/A')} | "
            f"Name: {product.get('product_name', 'Unknown')} | "
            f"Brand: {product.get('brands', 'Unknown')}"
        )

    print("-" * 60)

def import_external_product():
    barcode = input("Enter product barcode: ").strip()

    if not barcode:
        print("Barcode is required.")
        return

    response = requests.post(
        f"{BASE_URL}/products/import",
        json={"barcode": barcode}
    )

    if response.status_code == 201:
        result = response.json()

        print("\nProduct imported successfully.")
        print(result["item"])

    else:
        print(response.json().get(
            "error",
            "Failed to import product"
        ))

if __name__ == "__main__":
    main()