from fastapi import FastAPI, HTTPException 
from models import Department, Product

app = FastAPI()



@app.get("/")
async def root():
    return {"message": "Hello World"}

departments = []

# Get all departments
@app.get("/departments")
async def get_departments():
    return {"Departments": departments}

# Get single department
@app.get("/departments/{department_id}")
async def get_department(department_id: int):
    for department in departments:
        if department.id == department_id:
            return {"Department": department}
    raise HTTPException(status_code=404, detail="department not found")


# Create a department
@app.post("/departments")
async def create_department(department: Department):
    departments.append(department)
    return {"message": "Department has been added"}

# Update a department
@app.put("/departments/{department_id}")
async def update_department(department_id: int, department_obj: Department):
    for department in departments:
        if department.id == department_id:
            department.id = department_obj.id
            department.name = department_obj.name
            return {"Department": department}
        
    raise HTTPException(status_code=404, detail="department not found")

# Delete a department
@app.delete("/departments/{department_id}")
async def delete_department(department_id: int):
    for department in departments:
        if department.id == department_id:
            departments.remove(department)
            return {"message": "Department has been DELETED!"}
    return {"message": f"Department with id:{department_id} was not found"}


products = []

# Get all products
@app.get("/products")
async def get_products():
    return {"Products": products}

# Get single product
@app.get("/products/{product_id}")
async def get_product(product_id: int):
    for product in products:
        if product.id == product_id:
            return {"Products": product}
    return {"message": f"Product with id:{product_id} was not found"}

# Create a product
@app.post("/products")
async def create_product(product: Product):
    products.append(product)
    return {"message": "Product has been added"}

# Update a Product
@app.put("/products/{product_id}")
async def update_product(product_id: int, product_obj: Product):
    for product in products:
        if product.id == product_id:
            product.id == product_obj.id
            product.name = product_obj.name
            product.price = product_obj.price
            product.quantity = product_obj.quantity
            product.department_id = product_obj.department_id
            product.specifications = product_obj.specifications
            return {"Product": product}
    return {"message": "No Products found to update"}

# Delete a product
@app.delete("/products/{product_id}")
async def delete_product(product_id: int):
    for product in products:
        if product.id == product_id:
            products.remove(product)
            return {"message": "Product has been DELETED!"}
    return {"message": f"Product with id:{product_id} was not found"}


