from fastapi import FastAPI, HTTPException 
from models import Department, Product, UpdateProductInput
from store import Store
from Error import StoreExceptionInvalidID, StoreExceptionInvalidDepartmentID, StoreExceptionInvalidProductID
from stores_manager import StoresManager


app = FastAPI()
store_manager = StoresManager()


@app.get("/")
async def root():
    return {"message": "Welcome to store API"}

@app.delete("/")
async def reset_all():
    response = store_manager.reset_all()
    return {"message": response}


# Create a store
@app.post("/create_store")
async def create_store(name : str):
    response = store_manager.create_store(name)
    return {"message": response}

# Get all stores
@app.get("/stores")
async def get_stores():
    try:    
        all_stores = store_manager.get_all_stores()
        return {"Stores": all_stores}
    except Exception as ex:
            raise HTTPException(status_code=500, detail=str(ex))

# Delete a store    
@app.delete("/stores")
async def delete_store(store_id):
    try:  
        response = store_manager.delete_store(store_id)  
        return {"message": response}
    except StoreExceptionInvalidID as ex:
        raise HTTPException(status_code=404, detail=str(ex))
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


# Create a department
@app.post("/departments")
async def create_department(department: Department, store_id : int):
    try:  
        response = store_manager.create_department(department.department_name, store_id)
        return {"message": response}
    except StoreExceptionInvalidID as ex:
        raise HTTPException(status_code=404, detail=str(ex))
    
# Get all departments
@app.get("/departments")
async def get_departments():
    try:
        all_departments = store_manager.get_all_departments()
        return {"Departments": all_departments}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

# Get single department
@app.get("/departments/{department_id}")
async def get_department(department_id: int):
    try:
        response = store_manager.get_specific_department(department_id)
        return response
    except StoreExceptionInvalidDepartmentID as ex:
        raise HTTPException(status_code=404, detail=str(ex))
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Unknown Error: {ex}")

# Update a department
@app.put("/departments/{department_id}")
async def update_department(department_id: int, department_obj: Department):
    try:
        response = store_manager.update_department(department_id, department_obj.department_name)
        return {"message": response}
    except StoreExceptionInvalidDepartmentID as ex:
        raise HTTPException(status_code=404, detail=str(ex))
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

# Delete a department
@app.delete("/departments/{department_id}")
async def delete_department(department_id: int):
    try:
        response = store_manager.delete_department(department_id)
        return {"message": response}
    except StoreExceptionInvalidDepartmentID as ex:
        raise HTTPException(status_code=404, detail=str(ex))
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))



# Create a product
@app.post("/products")
async def create_product(product: Product, department_id: int):
    try:
        response = store_manager.create_product(product.product_name, product.price, product.quantity, product.specifications, department_id)
        return {"message": response}
    except StoreExceptionInvalidDepartmentID as ex:
        raise HTTPException(status_code=404, detail=str(ex))
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
    
# Get all products
@app.get("/products")
async def get_products():
    try:
        all_products = store_manager.get_all_products()
        return {"Products": all_products}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

# Get single product
@app.get("/products")
async def get_product(product_id: int):
    try:    
        response = store_manager.get_specific_product(product_id)
        return response
    except StoreExceptionInvalidProductID as ex:
        raise HTTPException(status_code=404, detail=str(ex))
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

# Update a Product
@app.put("/products/{product_id}")
async def update_product(product_id: int, product:UpdateProductInput):
    try:    
        response = store_manager.update_product(product_id, product.product_name, product.price, product.quantity, product.specifications)
        return {"message": response}
    except StoreExceptionInvalidProductID as ex:
        raise HTTPException(status_code=404, detail=str(ex))
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

# Delete a product
@app.delete("/products/{product_id}")
async def delete_product(product_id: int):
    try:
        response = store_manager.delete_product(product_id)
        return {"message": response}
    except StoreExceptionInvalidProductID as ex:
        raise HTTPException(status_code=404, detail=str(ex))
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
    










