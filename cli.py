import requests


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
    
def main():
    while True:
        show_menu()

        choice = input("Choose an option: ").strip()

        if choice == "1":
            display_inventory()

        elif choice == "6":
            print("Goodbye!")
            break

        else:
            print("Option not implemented yet.")


if __name__ == "__main__":
    main()