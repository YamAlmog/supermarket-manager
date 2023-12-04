from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from typing import List

class Store(BaseModel):
    store_id: int
    store_name: str

class Department(BaseModel):
    department_name: str 
    
class DepartmentDetails(Department):
    department_id: int
    store_id: int

class Product(BaseModel):
    product_name: str
    price: float
    quantity: int
    specifications: Optional[str] = None


class UpdateProductInput(BaseModel):
    product_name: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None
    specifications: Optional[str] = None


class ProductDetails(Product):
    product_id: int
    department_id: int


class StoreDetails(Store):
    products : List[ProductDetails]

