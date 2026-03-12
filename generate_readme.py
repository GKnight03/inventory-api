from datetime import datetime

content = f"""Inventory API README
Generated on: {datetime.now()}

Available Endpoints:

1. GET /getSingleProduct?id=1
   Returns one product by ProductID

2. GET /getAll
   Returns all products

3. POST /addNew
   Adds a new product
   Required JSON body:
   {{
      "ProductID": int,
      "Name": str,
      "UnitPrice": float,
      "StockQuantity": int,
      "Description": str
   }}

4. DELETE /deleteOne?id=1
   Deletes one product by ProductID

5. GET /startsWith?letter=S
   Returns products where Name starts with a given letter

6. GET /paginate?start=1&end=10
   Returns up to 10 products between ProductID range

7. GET /convert?id=1
   Returns the product price converted from USD to EUR

FastAPI interactive docs:
- http://localhost:8000/docs
- http://localhost:8000/redoc
"""

with open("README.txt", "w", encoding="utf-8") as file:
    file.write(content)

print("README.txt generated successfully.")