from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "inventorydb"
COLLECTION_NAME = "products"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
products_collection = db[COLLECTION_NAME]