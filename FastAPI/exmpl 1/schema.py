from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    
    name:str
    price: float
    in_stock: bool


