from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

class Department(BaseModel):
    name: str 
    


class Product(BaseModel):
    name: str
    price: float
    quantity: int
    department_id: int
    specifications: Optional[str] = None


