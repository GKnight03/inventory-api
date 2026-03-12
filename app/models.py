from pydantic import BaseModel, Field


class Product(BaseModel):
    ProductID: int = Field(..., gt=0)
    Name: str = Field(..., min_length=1)
    UnitPrice: float = Field(..., gt=0)
    StockQuantity: int = Field(..., ge=0)
    Description: str = Field(..., min_length=1)