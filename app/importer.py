import csv
from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "inventorydb"
COLLECTION_NAME = "products"
CSV_FILE = "data/products.csv"


def import_csv_to_mongodb():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    collection.delete_many({})

    products = []

    with open(CSV_FILE, "r", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        for row in reader:
            product = {
                "ProductID": int(row["ProductID"]),
                "Name": row["Name"],
                "UnitPrice": float(row["UnitPrice"]),
                "StockQuantity": int(row["StockQuantity"]),
                "Description": row["Description"]
            }
            products.append(product)

    if products:
        collection.insert_many(products)
        print(f"Imported {len(products)} products into MongoDB.")
    else:
        print("No products found in CSV.")


if __name__ == "__main__":
    import_csv_to_mongodb()