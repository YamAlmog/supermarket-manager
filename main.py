from fastapi import FastAPI, HTTPException 
from models import Department, Product
from store import Store

app = FastAPI()
store = Store()

@app.get("/")
async def root():
    return {"message": "Welcome to store API"}

# clean global variables
@app.delete("/")
async def clean_departments_and_products():
    return store.set_up_store()

# Get all departments
@app.get("/departments")
async def get_departments():
    return {"Departments": store.departments}

# Get single department
@app.get("/departments/{department_id}")
async def get_department(department_id: int):
    response = store.get_department(department_id)
    return response

# Create a department
@app.post("/departments")
async def create_department(department: Department):
    response = store.create_department(department.name)
    return response


# Update a department
@app.put("/departments/{department_id}")
async def update_department(department_id: int, department_obj: Department):
    response = store.update_department(department_id, department_obj.name)
    return response


# Delete a department
@app.delete("/departments/{department_id}")
async def delete_department(department_id: int):
    response = store.delete_department(department_id)
    return response


# Get all products
@app.get("/products")
async def get_products():
    return {"Products": store.products}

# Get single product
@app.get("/products/{product_id}")
async def get_product(product_id: int):
    response = store.get_selected_product(product_id)
    return response


# Create a product
@app.post("/products")
async def create_product(product: Product):
    response = store.create_product(product)
    return response


# Update a Product
@app.put("/products/{product_id}")
async def update_product(product_id: int, product_obj: Product):
    response= store.update_selected_product(product_id, product_obj)
    return response


# Delete a product
@app.delete("/products/{product_id}")
async def delete_product(product_id: int):
    response = store.delete_selected_product(product_id)
    return response








