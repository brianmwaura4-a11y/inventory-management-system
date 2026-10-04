# Inventory Management System

A Flask REST API and command-line interface (CLI) for managing inventory for a small retail company.

The system provides full CRUD operations for inventory items, input validation, error handling, product search through the OpenFoodFacts API, product importing, and automated tests.

---

## Table of Contents

* [Project Overview](#project-overview)
* [Features](#features)
* [Technologies](#technologies)
* [Project Structure](#project-structure)
* [Installation](#installation)
* [Running the Application](#running-the-application)
* [REST API](#rest-api)
* [Inventory Endpoints](#inventory-endpoints)
* [OpenFoodFacts Endpoints](#openfoodfacts-endpoints)
* [CLI](#cli)
* [Validation and Error Handling](#validation-and-error-handling)
* [Testing](#testing)
* [Git Workflow](#git-workflow)
* [Future Improvements](#future-improvements)
* [Author](#author)

---

## Project Overview

The Inventory Management System is designed for a small retail business that needs a simple way to manage its products.

The application provides:

1. A Flask REST API for inventory management.
2. CRUD operations for inventory items.
3. Search functionality for local inventory.
4. Integration with the OpenFoodFacts API.
5. The ability to search products by name.
6. The ability to retrieve products using a barcode.
7. The ability to import external products into the local inventory.
8. A CLI for interacting with the application.
9. Automated unit and integration tests.

The inventory is currently stored in an in-memory Python list.

---

## Features

### Inventory Management

* View all inventory items.
* View an individual inventory item.
* Create new inventory items.
* Update existing inventory items.
* Delete inventory items.
* Search inventory by product name.

### Validation

The API validates:

* Required fields.
* Quantity values.
* Price values.
* Duplicate barcodes.
* Valid update fields.
* Required search parameters.
* Required barcode values.

### Error Handling

The API provides appropriate HTTP status codes for common errors, including:

* `200 OK`
* `201 Created`
* `400 Bad Request`
* `404 Not Found`
* `409 Conflict`
* `502 Bad Gateway`

### OpenFoodFacts Integration

The application integrates with OpenFoodFacts to:

* Search for products by name.
* Retrieve product information by barcode.
* Import external products into the local inventory.

### CLI

The command-line interface allows users to:

* View inventory.
* View individual products.
* Add products.
* Update products.
* Delete products.
* Search OpenFoodFacts.
* Import products from OpenFoodFacts.

### Testing

The project includes automated tests for:

* Inventory CRUD operations.
* Validation.
* Error handling.
* Inventory search.
* External API functionality.
* Product importing.
* CLI functionality.

---

## Technologies

* Python 3
* Flask
* Requests
* Pytest
* OpenFoodFacts API
* Git
* GitHub

---

## Project Structure

```text
inventory-management-system/
│
├── app.py
├── cli.py
├── external_api.py
├── requirements.txt
├── README.md
│
├── data/
│   ├── __init__.py
│   └── inventory.py
│
└── tests/
    ├── __init__.py
    ├── test_inventory.py
    ├── test_external_api.py
    └── test_cli.py
```

### Main Files

#### `app.py`

Contains the Flask application and REST API routes.

#### `cli.py`

Contains the command-line interface used to interact with the Flask API.

#### `external_api.py`

Contains helper functions for communicating with the OpenFoodFacts API.

#### `data/inventory.py`

Contains the application's inventory data.

#### `tests/`

Contains automated tests for the API, external API integration, and CLI.

#### `requirements.txt`

Contains the Python dependencies required to run the project.

---

# Installation

## 1. Clone the Repository

```bash
git clone <your-repository-url>
```

Navigate into the project:

```bash
cd inventory-management-system
```

---

## 2. Create a Virtual Environment

```bash
python3 -m venv .venv
```

---

## 3. Activate the Virtual Environment

On Linux/macOS:

```bash
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

---

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` does not exist yet, install the main dependencies:

```bash
pip install flask requests pytest
```

Then generate the requirements file:

```bash
pip freeze > requirements.txt
```

---

# Running the Application

## Start the Flask Server

Run:

```bash
python app.py
```

The application will start at:

```text
http://127.0.0.1:5000
```

Keep this terminal running.

---

# REST API

The application provides the following routes:

| Method | Endpoint                        | Description                     |
| ------ | ------------------------------- | ------------------------------- |
| GET    | `/inventory`                    | Get all inventory items         |
| GET    | `/inventory/<id>`               | Get one inventory item          |
| POST   | `/inventory`                    | Create an inventory item        |
| PATCH  | `/inventory/<id>`               | Update an inventory item        |
| DELETE | `/inventory/<id>`               | Delete an inventory item        |
| GET    | `/inventory/search?name=<name>` | Search local inventory          |
| GET    | `/products/search?name=<name>`  | Search OpenFoodFacts            |
| GET    | `/products/barcode/<barcode>`   | Get external product by barcode |
| POST   | `/products/import`              | Import an external product      |

---

# Inventory Endpoints

## 1. Get All Inventory

### Request

```http
GET /inventory
```

### Example

```bash
curl http://127.0.0.1:5000/inventory
```

### Response

```json
[
    {
        "id": 1,
        "name": "Coca Cola",
        "category": "Beverages",
        "barcode": "5449000000996",
        "quantity": 20,
        "price": 150.0
    },
    {
        "id": 2,
        "name": "Nutella",
        "category": "Spreads",
        "barcode": "3017620422003",
        "quantity": 10,
        "price": 650.0
    }
]
```

---

## 2. Get One Inventory Item

### Request

```http
GET /inventory/<id>
```

### Example

```bash
curl http://127.0.0.1:5000/inventory/1
```

### Successful Response

```json
{
    "id": 1,
    "name": "Coca Cola",
    "category": "Beverages",
    "barcode": "5449000000996",
    "quantity": 20,
    "price": 150.0
}
```

### Item Not Found

```json
{
    "error": "Inventory item not found"
}
```

Status:

```text
404 Not Found
```

---

## 3. Create an Inventory Item

### Request

```http
POST /inventory
```

### Example

```bash
curl -X POST http://127.0.0.1:5000/inventory \
-H "Content-Type: application/json" \
-d '{
    "name": "Pepsi",
    "category": "Beverages",
    "barcode": "123456789",
    "quantity": 15,
    "price": 100
}'
```

### Successful Response

```json
{
    "id": 3,
    "name": "Pepsi",
    "category": "Beverages",
    "barcode": "123456789",
    "quantity": 15,
    "price": 100
}
```

Status:

```text
201 Created
```

---

## 4. Update an Inventory Item

The API uses `PATCH`, allowing individual fields to be updated.

### Request

```http
PATCH /inventory/<id>
```

### Example

```bash
curl -X PATCH http://127.0.0.1:5000/inventory/1 \
-H "Content-Type: application/json" \
-d '{
    "quantity": 50
}'
```

### Response

```json
{
    "id": 1,
    "name": "Coca Cola",
    "category": "Beverages",
    "barcode": "5449000000996",
    "quantity": 50,
    "price": 150.0
}
```

Status:

```text
200 OK
```

---

## 5. Delete an Inventory Item

### Request

```http
DELETE /inventory/<id>
```

### Example

```bash
curl -X DELETE http://127.0.0.1:5000/inventory/1
```

### Response

```json
{
    "message": "Inventory item deleted successfully"
}
```

Status:

```text
200 OK
```

---

## 6. Search Local Inventory

Inventory can be searched by product name.

### Request

```http
GET /inventory/search?name=<name>
```

### Example

```bash
curl "http://127.0.0.1:5000/inventory/search?name=coca"
```

The search is case-insensitive and supports partial matches.

For example:

```text
coca
```

can match:

```text
Coca Cola
```

---

# OpenFoodFacts Endpoints

The application integrates with the OpenFoodFacts API to retrieve product information.

The integration uses the OpenFoodFacts API v2.

---

## 1. Search OpenFoodFacts

### Request

```http
GET /products/search?name=<name>
```

### Example

```bash
curl "http://127.0.0.1:5000/products/search?name=nutella"
```

The application returns matching products containing information such as:

* Barcode
* Product name
* Brand
* Category

---

## 2. Get Product by Barcode

### Request

```http
GET /products/barcode/<barcode>
```

### Example

```bash
curl http://127.0.0.1:5000/products/barcode/3017624010701
```

The application requests product information from OpenFoodFacts and returns the product information.

If the product does not exist:

```json
{
    "error": "Product not found on OpenFoodFacts"
}
```

Status:

```text
404 Not Found
```

If the external service fails:

```json
{
    "error": "External API request failed: ..."
}
```

Status:

```text
502 Bad Gateway
```

---

# Import Product from OpenFoodFacts

Products found through OpenFoodFacts can be imported into the local inventory.

## Request

```http
POST /products/import
```

### Request Body

```json
{
    "barcode": "3017624010701"
}
```

### Example

```bash
curl -X POST http://127.0.0.1:5000/products/import \
-H "Content-Type: application/json" \
-d '{
    "barcode": "3017624010701"
}'
```

### Response

```json
{
    "message": "Product imported successfully",
    "item": {
        "id": 3,
        "name": "Nutella",
        "category": "Spreads",
        "barcode": "3017624010701",
        "quantity": 0,
        "price": 0,
        "brand": "Ferrero"
    }
}
```

Status:

```text
201 Created
```

The imported product starts with:

```text
quantity = 0
price = 0
```

These values can subsequently be updated using the inventory `PATCH` endpoint.

---

# Validation and Error Handling

The API validates incoming data before modifying the inventory.

## Required Fields

Creating an inventory item requires:

```text
name
category
barcode
quantity
price
```

If a required field is missing:

```json
{
    "error": "Missing required field: name"
}
```

Status:

```text
400 Bad Request
```

---

## Quantity Validation

Quantity must be a non-negative integer.

Invalid:

```json
{
    "quantity": -5
}
```

Response:

```json
{
    "error": "Quantity must be a non-negative integer"
}
```

---

## Price Validation

Price must be a non-negative number.

Invalid:

```json
{
    "price": -100
}
```

Response:

```json
{
    "error": "Price must be a non-negative number"
}
```

---

## Duplicate Barcode Validation

Each inventory item must have a unique barcode.

Attempting to add an existing barcode returns:

```json
{
    "error": "An item with this barcode already exists"
}
```

Status:

```text
409 Conflict
```

---

## Invalid Update Fields

Only the following fields can be updated:

```text
name
category
barcode
quantity
price
```

Attempting to update an invalid field returns:

```json
{
    "error": "Invalid field: invalid_field"
}
```

Status:

```text
400 Bad Request
```

---

# CLI

The application includes a command-line interface that communicates with the Flask REST API.

## Start the API

In the first terminal:

```bash
python app.py
```

Keep the server running.

## Start the CLI

Open a second terminal.

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Run:

```bash
python cli.py
```

---

## CLI Menu

The CLI provides the following options:

```text
1. View inventory
2. Get inventory item
3. Add inventory item
4. Update inventory item
5. Delete inventory item
6. Exit
7. Search OpenFoodFacts
8. Import product from OpenFoodFacts
```

The CLI sends HTTP requests to the Flask API rather than directly modifying the inventory data.

This keeps the application architecture separated into:

```text
CLI
  |
  | HTTP requests
  v
Flask REST API
  |
  v
Inventory
```

For external products:

```text
CLI
  |
  v
Flask REST API
  |
  v
OpenFoodFacts API
```

---

# Testing

The project uses **pytest** for automated testing.

Run the complete test suite:

```bash
pytest -v
```

Alternatively:

```bash
python -m pytest -v
```

---

## Test Files

### `tests/test_inventory.py`

Tests:

* Get all inventory.
* Get an individual item.
* Missing inventory item.
* Create inventory item.
* Missing required fields.
* Duplicate barcodes.
* Invalid quantity.
* Update inventory.
* Update multiple fields.
* Invalid update fields.
* Delete inventory.
* Delete missing items.
* Search inventory.

### `tests/test_external_api.py`

Tests:

* External API barcode lookup.
* Product-not-found responses.
* External product search.
* Missing search name.
* Product import.
* Duplicate product import.
* Flask external API routes.

External API requests are mocked during tests so that tests do not depend on the availability of the real OpenFoodFacts service.

### `tests/test_cli.py`

Tests:

* Getting inventory through the API.
* Creating inventory items.
* Updating inventory items.
* Deleting inventory items.
* Searching OpenFoodFacts.
* Importing OpenFoodFacts products.

---

# API Architecture

The project follows a simple client-server architecture.

```text
                ┌───────────────┐
                │     CLI       │
                └───────┬───────┘
                        │
                        │ HTTP
                        ▼
                ┌───────────────┐
                │ Flask REST API│
                │    app.py     │
                └───────┬───────┘
                        │
             ┌──────────┴──────────┐
             │                     │
             ▼                     ▼
      ┌─────────────┐      ┌─────────────────┐
      │  Inventory  │      │ OpenFoodFacts   │
      │   Data      │      │      API        │
      └─────────────┘      └─────────────────┘
```

The Flask application acts as the central API layer.

The CLI communicates with Flask through HTTP requests.

The Flask application communicates with OpenFoodFacts when external product information is required.

---

# Git Workflow

The project was developed using feature branches.

The main development branches were:

```text
main
│
├── feature/flask-api
│
├── feature/external-api
│
├── feature/cli
│
└── feature/tests
```

## Feature Branches

### `feature/flask-api`

Used for:

* Flask application setup.
* Inventory CRUD.
* Inventory search.
* Input validation.
* Error handling.

### `feature/external-api`

Used for:

* OpenFoodFacts integration.
* Barcode lookup.
* Product search.
* Product importing.

### `feature/cli`

Used for:

* Command-line interface.
* API communication from the CLI.
* Inventory management through the terminal.

### `feature/tests`

Used for:

* Inventory tests.
* External API tests.
* CLI tests.
* Mocking external HTTP requests.

Each feature was committed separately and pushed to GitHub.

---

# Example Git Commands

Create a feature branch:

```bash
git switch -c feature/example
```

Check the current branch:

```bash
git branch
```

Check changes:

```bash
git status
```

Stage changes:

```bash
git add .
```

Commit changes:

```bash
git commit -m "Add feature"
```

Push the feature branch:

```bash
git push -u origin feature/example
```

After completing a feature, the branch can be submitted as a pull request for review and merged into `main`.

---

# Future Improvements

Possible future improvements include:

* Persistent database storage.
* User authentication and authorization.
* Inventory categories.
* Stock alerts.
* Product price history.
* Pagination.
* API documentation using Swagger/OpenAPI.
* Docker support.
* Deployment to a cloud platform.
* A web-based frontend.
* Improved product validation.
* Inventory reporting and analytics.

---

# Author

**Brian Mwaura**

Software Engineering Student

This project was developed as part of a Python and Flask REST API learning project.
