from fastapi import FastAPI
from pydantic import BaseModel


class Department(BaseModel):
    name: str 
    


class Product(BaseModel):
    name: str
    price: float
    quantity: int
    department_id: int
    specifications: str


