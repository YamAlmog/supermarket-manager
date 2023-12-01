from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

class Department(BaseModel):
    department_name: str 
    


class Product(BaseModel):
    product_name: str
    price: float
    quantity: int
    department_id: int
    store_id: int
    specifications: Optional[str] = None


