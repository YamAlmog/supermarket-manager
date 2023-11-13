from fastapi import FastAPI
from pydantic import BaseModel

class Department(BaseModel):
    id: int
    name: str 


class Product(BaseModel):
    id: int
    name: str
    price: float
    quantity: int
    department_id: int
    specifications: str


