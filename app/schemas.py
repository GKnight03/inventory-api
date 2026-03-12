def product_serializer(product) -> dict:
    return {
        "ProductID": product["ProductID"],
        "Name": product["Name"],
        "UnitPrice": product["UnitPrice"],
        "StockQuantity": product["StockQuantity"],
        "Description": product["Description"],
    }


def products_serializer(products) -> list:
    return [product_serializer(product) for product in products]