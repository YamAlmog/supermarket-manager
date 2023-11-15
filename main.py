from fastapi import FastAPI, HTTPException 
from models import Department, Product

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

# init dict of departments and index for the department in dict
departments = {}
dep_count = 0

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
    global dep_count
    departments[dep_count]= department.name
    dep_count += 1
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
        departments.pop(department_id)
        return {"message": f"Department id: {department_id} has been DELETED!"}
    raise HTTPException(status_code=404, detail="Department not found")

# init products dict and a counter for the products
products = {}
prod_count = 0

# Get all products
@app.get("/products")
async def get_products():
    return {"Products": products}

# Get single product
@app.get("/products/{product_id}")
async def get_product(product_id: int):
    if product_id in products:
        key = product_id
        value = products[product_id]
        return {"Products": {"Key": key, "Value": value}}
        
    raise HTTPException(status_code=404, detail="Product not found")

# Create a product
@app.post("/products")
async def create_product(product: Product):
    global prod_count
    name = product.name
    price = product.price
    quantity = product.quantity
    department_id = product.department_id
    specifications = product.specifications
    if department_id not in departments:
        raise HTTPException(status_code=400, detail=f"There is no Department with id:{department_id}")
    else:
        prod_tuple = (name, price, quantity, department_id, specifications)
        products[prod_count] = prod_tuple
        prod_count += 1
        return {"message": "Product has been added"}

# Update a Product
@app.put("/products/{product_id}")
async def update_product(product_id: int, product_obj: Product):
    if product_id in products:
        name = product_obj.name
        price = product_obj.price
        quantity = product_obj.quantity
        department_id = product_obj.department_id
        specifications = product_obj.specifications
        if department_id not in departments:
            raise HTTPException(status_code=400, detail=f"There is no Department with id:{department_id}")    
        else:    
            put_tuple = (name, price, quantity, department_id, specifications)
            products[product_id] = put_tuple
            return {"Product": {"Key": product_id, "Value": put_tuple}}
    raise HTTPException(status_code=404, detail="Product not found")

# Delete a product
@app.delete("/products/{product_id}")
async def delete_product(product_id: int):
    if product_id in products: 
        products.pop(product_id)
        return {"message": f"Products id: {product_id} has been DELETED!"}
    raise HTTPException(status_code=404, detail="Product not found")


