from fastapi import FastAPI, HTTPException 
from models import Department, Product
from store import Store
from Error import StoreException, StoreExceptionInvalidID

app = FastAPI()
store = Store()


@app.get("/")
async def root():
    return {"message": "Welcome to store API"}

# clean global variables
@app.delete("/")
async def clean_departments_and_products():
    return store.reset_store()

# Get all departments
@app.get("/departments")
async def get_departments():
    return {"Departments": store.departments}

# Get single department
@app.get("/departments/{department_id}")
async def get_department(department_id: int):
    try:
        response = store.get_department(department_id)
        return response
    except StoreException as ex:
        raise HTTPException(status_code=404, detail=str(ex))
    

# Create a department
@app.post("/departments")
async def create_department(department: Department):
    response = store.create_department(department.name)
    return response


# Update a department
@app.put("/departments/{department_id}")
async def update_department(department_id: int, department_obj: Department):
    try:
        response = store.update_department(department_id, department_obj.name)
        return response
    except StoreException as ex:
        raise HTTPException(status_code=404, detail=str(ex))
    


# Delete a department
@app.delete("/departments/{department_id}")
async def delete_department(department_id: int):
    try:
        response = store.delete_department(department_id)
        return response
    except StoreException as ex:
        raise HTTPException(status_code=404, detail=str(ex))

# Get all products
@app.get("/products")
async def get_products():
    return {"Products": store.products}

# Get single product
@app.get("/products/{product_id}")
async def get_product(product_id: int):
    try:    
        response = store.get_selected_product(product_id)
        return response
    except StoreException as ex:
        raise HTTPException(status_code=404, detail=str(ex))


# Create a product
@app.post("/products")
async def create_product(product: Product):
    try:
        response = store.create_product(product)
        return response
    except StoreExceptionInvalidID as ex:
        raise HTTPException(status_code=400, detail=str(ex))

# Update a Product
@app.put("/products/{product_id}")
async def update_product(product_id: int, product_obj: Product):
    try:    
        response = store.update_selected_product(product_id, product_obj)
        return response
    except StoreExceptionInvalidID as ex:
        raise HTTPException(status_code=400, detail=str(ex))
    except StoreException as ex:
        raise HTTPException(status_code=404, detail=str(ex))

# Delete a product
@app.delete("/products/{product_id}")
async def delete_product(product_id: int):
    try:
        response = store.delete_selected_product(product_id)
        return response
    except StoreException as ex:
        raise HTTPException(status_code=404, detail=str(ex))








