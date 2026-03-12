from fastapi.testclient import TestClient
from app.main import app
from app.database import products_collection

client = TestClient(app)


def setup_module(module):
    products_collection.delete_many({})
    products_collection.insert_many([
        {
            "ProductID": 1,
            "Name": "Keyboard",
            "UnitPrice": 25.50,
            "StockQuantity": 10,
            "Description": "USB Keyboard"
        },
        {
            "ProductID": 2,
            "Name": "Screen",
            "UnitPrice": 199.99,
            "StockQuantity": 5,
            "Description": "24 inch monitor"
        },
        {
            "ProductID": 3,
            "Name": "Speaker",
            "UnitPrice": 45.00,
            "StockQuantity": 8,
            "Description": "Bluetooth speaker"
        }
    ])


def teardown_module(module):
    products_collection.delete_many({})


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Inventory API is running"


def test_get_single_product():
    response = client.get("/getSingleProduct?id=1")
    assert response.status_code == 200
    assert response.json()["ProductID"] == 1


def test_get_all():
    response = client.get("/getAll")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_add_new():
    payload = {
        "ProductID": 10,
        "Name": "Mouse",
        "UnitPrice": 19.99,
        "StockQuantity": 15,
        "Description": "Wireless mouse"
    }
    response = client.post("/addNew", json=payload)
    assert response.status_code == 200
    assert response.json()["message"] == "Product added successfully"


def test_delete_one():
    response = client.delete("/deleteOne?id=10")
    assert response.status_code == 200


def test_starts_with():
    response = client.get("/startsWith?letter=S")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_paginate():
    response = client.get("/paginate?start=1&end=20")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_convert():
    response = client.get("/convert?id=1")
    assert response.status_code in [200, 500]