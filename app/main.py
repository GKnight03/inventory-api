from fastapi import FastAPI, HTTPException, Query
from app.database import products_collection
from app.models import Product
from app.schemas import product_serializer, products_serializer
from app.currency import convert_usd_to_eur
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("inventory-api")

app = FastAPI(title="Inventory API", version="1.0")


@app.get("/")
def home():
    return {"message": "Inventory API is running"}


@app.get("/getSingleProduct")
def get_single_product(id: int = Query(..., gt=0)):
    product = products_collection.find_one({"ProductID": id})
    if product:
        return product_serializer(product)
    raise HTTPException(status_code=404, detail="Product not found")


@app.get("/getAll")
def get_all_products():
    products = products_collection.find()
    return products_serializer(products)


@app.post("/addNew")
def add_new_product(product: Product):
    existing = products_collection.find_one({"ProductID": product.ProductID})
    if existing:
        raise HTTPException(status_code=400, detail="ProductID already exists")

    product_data = product.model_dump()
    products_collection.insert_one(product_data)

    return {
        "message": "Product added successfully",
        "product": {
            "ProductID": product_data["ProductID"],
            "Name": product_data["Name"],
            "UnitPrice": product_data["UnitPrice"],
            "StockQuantity": product_data["StockQuantity"],
            "Description": product_data["Description"]
        }
    }


@app.delete("/deleteOne")
def delete_one_product(id: int = Query(..., gt=0)):
    result = products_collection.delete_one({"ProductID": id})
    if result.deleted_count == 1:
        return {"message": f"Product with ID {id} deleted successfully"}
    raise HTTPException(status_code=404, detail="Product not found")


@app.get("/startsWith")
def starts_with(letter: str = Query(..., min_length=1, max_length=1)):
    regex_pattern = f"^{letter}"
    products = products_collection.find({"Name": {"$regex": regex_pattern, "$options": "i"}})
    return products_serializer(products)


@app.get("/paginate")
def paginate_products(
    start: int = Query(..., gt=0),
    end: int = Query(..., gt=0)
):
    if start > end:
        raise HTTPException(status_code=400, detail="Start ID must be less than or equal to end ID")

    products = products_collection.find(
        {"ProductID": {"$gte": start, "$lte": end}}
    ).sort("ProductID", 1).limit(10)

    return products_serializer(products)


@app.get("/convert")
def convert_price(id: int = Query(..., gt=0)):
    product = products_collection.find_one({"ProductID": id})
    if not product:
        logger.error(f"Product not found for ProductID {id}")
        raise HTTPException(status_code=404, detail="Product not found")

    try:
        logger.debug(f"Product fetched: {product}")
        usd_price = product.get("UnitPrice")
        if usd_price is None:
            logger.error(f"UnitPrice missing for ProductID {id}")
            raise HTTPException(status_code=500, detail="UnitPrice missing in product data.")
        if not isinstance(usd_price, (int, float)):
            logger.error(f"UnitPrice not a number for ProductID {id}: {usd_price}")
            raise HTTPException(status_code=500, detail="UnitPrice is not a valid number.")
        logger.debug(f"USD Price: {usd_price}")
        eur_price = convert_usd_to_eur(usd_price)
        logger.debug(f"EUR Price: {eur_price}")
        return {
            "ProductID": product["ProductID"],
            "Name": product["Name"],
            "PriceUSD": usd_price,
            "PriceEUR": eur_price
        }
    except Exception as e:
        logger.exception(f"Currency conversion failed for ProductID {id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Currency conversion failed: {str(e)}")