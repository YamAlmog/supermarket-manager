
from fastapi import HTTPException
from models import Department, Product

class Store:
    def __init__(self):
        self.departments = {}
        self.products = {}
        self.department_count = 0
        self.product_count = 0

    def set_up_store(self):
        self.departments = {}
        self.products = {}
        self.department_count = 0
        self.product_count = 0
        return {"message": "Cleaning the departments and products"}

    def create_department(self, name):
        self.departments[self.department_count]= name
        self.department_count += 1
        return {"message": "Department has been added"}

    def get_department(self, department_id):
        if department_id in self.departments:
            key = department_id
            value = self.departments[department_id]
            return {"Department": {"Key": key, "Value": value}}
    
        raise HTTPException(status_code=404, detail="Department not found")
    
    def update_department(self, department_id, name):
        if department_id in self.departments:
            self.departments[department_id] = name
            key = department_id
            value = self.departments[department_id]
            return {"Department": {"Key": key, "Value": value}}
        
        raise HTTPException(status_code=404, detail="Department not found")

    def delete_department(self, department_id):
        if department_id in self.departments: 
            self.departments.pop(department_id)
            return {"message": f"Department id: {department_id} has been DELETED!"}
        raise HTTPException(status_code=404, detail="Department not found")
    

    def create_product(self, product: Product):
        name = product.name
        price = product.price
        quantity = product.quantity
        department_id = product.department_id
        specifications = product.specifications
        if department_id not in self.departments:
            raise HTTPException(status_code=400, detail=f"There is no Department with id:{department_id}")
        else:
            prod_tuple = (name, price, quantity, department_id, specifications)
            self.products[self.product_count] = prod_tuple
            self.product_count += 1
            return {"message": "Product has been added"}


    def get_selected_product(self, product_id):
        if product_id in self.products:
            key = product_id
            value = self.products[product_id]
            return {"Products": {"Key": key, "Value": value}}
        
        raise HTTPException(status_code=404, detail="Product not found")
    
    def update_selected_product(self, product_id, product: Product):
        if product_id in self.products:
            name = product.name
            price = product.price
            quantity = product.quantity
            department_id = product.department_id
            specifications = product.specifications
            if department_id not in self.departments:
                raise HTTPException(status_code=400, detail=f"There is no Department with id:{department_id}")    
            else:    
                put_tuple = (name, price, quantity, department_id, specifications)
                self.products[product_id] = put_tuple
                return {"Product": {"Key": product_id, "Value": put_tuple}}
        raise HTTPException(status_code=404, detail="Product not found")
    
    def delete_selected_product(self, product_id):
        if product_id in self.products: 
            self.products.pop(product_id)
            return {"message": f"Products id: {product_id} has been DELETED!"}
        raise HTTPException(status_code=404, detail="Product not found")
