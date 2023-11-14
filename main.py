from fastapi import FastAPI, HTTPException 
from models import Department, Product

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

# init dict of departments
departments = {}
index = 0

# Get all departments
@app.get("/departments")
async def get_departments():
    return {"Departments": departments}

# Get single department
@app.get("/departments/{department_id}")
async def get_department(department_id: int):
    if department_id in departments:
        key = department_id
        value = departments[department_id]
        return {"Department": {"Key": key, "Value": value}}
        
    raise HTTPException(status_code=404, detail="Department not found")


# Create a department
@app.post("/departments")
async def create_department(department: Department):
    global index
    departments[index]= department.name
    index += 1
    return {"message": "Department has been added"}

# Update a department
@app.put("/departments/{department_id}")
async def update_department(department_id: int, department_obj: Department):
    if department_id in departments:
        departments[department_id] = department_obj.name
        key = department_id
        value = departments[department_id]
        return {"Department": {"Key": key, "Value": value}}
        
    raise HTTPException(status_code=404, detail="Department not found")

# Delete a department
@app.delete("/departments/{department_id}")
async def delete_department(department_id: int):
    if department_id in departments: 
        dep_value = departments.pop(department_id)
        return {"message": f"Department {dep_value} has been DELETED!"}
    raise HTTPException(status_code=404, detail="Department not found")


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
    raise HTTPException(status_code=404, detail="Product not found")

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
    raise HTTPException(status_code=404, detail="Product not found")

# Delete a product
@app.delete("/products/{product_id}")
async def delete_product(product_id: int):
    for product in products:
        if product.id == product_id:
            products.remove(product)
            return {"message": "Product has been DELETED!"}
    raise HTTPException(status_code=404, detail="Product not found")


