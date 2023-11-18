from fastapi import FastAPI, HTTPException 
from models import Department, Product
from store import Store
from Error import StoreException, StoreExceptionInvalidID

app = FastAPI()

stores = {
    # id1 : store1
    # id2 : store2
}
store_count = 0

@app.get("/")
async def root():
    return {"message": "Welcome to store API"}

# create stores
@app.post("/create_store")
async def create_store(name : str):
    global store_count
    new_store = Store(name)
    stores[store_count] = new_store
    store_count += 1
    return {"store has been created"}


@app.get("/stores")
async def get_stores():
    return {"Stores": stores}
    

# clean global variables
@app.delete("/")
async def clean_departments_and_products():
    global stores
    global store_count
    stores = {}
    store_count = 0
    return {"message": "Cleaning the departments and products"}

# Get all departments
@app.get("/departments")
async def get_departments(store_id: int):
    try:
        return {"Departments": stores[store_id].departments}
    except KeyError as ex:
        raise HTTPException(status_code=404, detail="Store not found")

# Get single department
@app.get("/departments/{department_id}")
async def get_department(department_id: int, store_id: int):
    try:
        response = stores[store_id].get_department(department_id)
        return response
    except StoreException as ex:
        raise HTTPException(status_code=404, detail=str(ex))
    except KeyError as ex:
        raise HTTPException(status_code=404, detail="Store not found")
    except Exception as ex:
        raise HTTPException(status_code=404, detail=f"Unkown Error: {ex}")

    

# Create a department
@app.post("/departments")
async def create_department(department: Department, store_id : int):
    try:    
        response = stores[store_id].create_department(department.name)
        return response
    except KeyError as ex:
        raise HTTPException(status_code=404, detail="Store not found")
    

# Update a department
@app.put("/departments/{department_id}")
async def update_department(store_id: int, department_id: int, department_obj: Department):
    try:
        response = stores[store_id].update_department(department_id, department_obj.name)
        return response
    except StoreException as ex:
        raise HTTPException(status_code=404, detail=str(ex))
    except KeyError as ex:
        raise HTTPException(status_code=404, detail="Store not found")


# Delete a department
@app.delete("/departments/{department_id}")
async def delete_department(store_id: int, department_id: int):
    try:
        response = stores[store_id].delete_department(department_id)
        return response
    except StoreException as ex:
        raise HTTPException(status_code=404, detail=str(ex))
    except KeyError as ex:
        raise HTTPException(status_code=404, detail="Store not found")

# Get all products
@app.get("/products")
async def get_products(store_id: int):
    try:
        return {"Products": stores[store_id].products}
    except KeyError as ex:
        raise HTTPException(status_code=404, detail="Store not found")


# Get single product
@app.get("/products/{product_id}")
async def get_product(store_id: int, product_id: int):
    try:    
        response = stores[store_id].get_selected_product(product_id)
        return response
    except StoreException as ex:
        raise HTTPException(status_code=404, detail=str(ex))
    except KeyError as ex:
        raise HTTPException(status_code=404, detail="Store not found")
    

# Create a product
@app.post("/products")
async def create_product(store_id: int, product: Product):
    try:
        response = stores[store_id].create_product(product)
        return response
    except StoreExceptionInvalidID as ex:
        raise HTTPException(status_code=400, detail=str(ex))
    except KeyError as ex:
        raise HTTPException(status_code=404, detail="Store not found")
    

# Update a Product
@app.put("/products/{product_id}")
async def update_product(store_id: int, product_id: int, product_obj: Product):
    try:    
        response = stores[store_id].update_selected_product(product_id, product_obj)
        return response
    except StoreExceptionInvalidID as ex:
        raise HTTPException(status_code=400, detail=str(ex))
    except StoreException as ex:
        raise HTTPException(status_code=404, detail=str(ex))
    except KeyError as ex:
        raise HTTPException(status_code=404, detail="Store not found")

# Delete a product
@app.delete("/products/{product_id}")
async def delete_product(store_id: int, product_id: int):
    try:
        response = stores[store_id].delete_selected_product(product_id)
        return response
    except StoreException as ex:
        raise HTTPException(status_code=404, detail=str(ex))
    except KeyError as ex:
        raise HTTPException(status_code=404, detail="Store not found")








