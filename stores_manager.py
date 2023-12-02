
import psycopg2
from Error import StoreExceptionInvalidID, StoreException, StoreExceptionInvalidDepartmentID, StoreExceptionInvalidProductID


class StoresManager:

    def __init__(self):
        # Initialize db connections 
        self.db_params = {
            'host': 'localhost',
            'port': 5432,
            'database': 'Learning',
            'user': 'postgres',
            'password': '123456',
        }

    # create new store. return store id
    def create_store(self, name: str):
        with psycopg2.connect(**self.db_params) as conn:
            cursor = conn.cursor()
            QUERY = f"INSERT INTO store (store_name) VALUES ('{name}')"

            cursor.execute(QUERY)
            conn.commit()
            cursor.close()
            return {"message": "Store has been created"}

    # return all stores
    def get_all_stores(self):
        with psycopg2.connect(**self.db_params) as conn:
            cursor = conn.cursor()
            QUERY = f"Select * from store"

            cursor.execute(QUERY)
            results = cursor.fetchall()
            cursor.close()
            return results
        
    # delete specific store included its department and product
    def delete_store(self, store_id: int) :
        with psycopg2.connect(**self.db_params) as conn:
            cursor = conn.cursor()
            IS_STORE_EXIST = f"SELECT EXISTS (SELECT 1 FROM store WHERE store_id = {store_id});"
            cursor.execute(IS_STORE_EXIST)
            is_exist = cursor.fetchone()
            if is_exist[0] == True:
                delete_store = f"DELETE FROM store WHERE store_id='{store_id}';"
                delete_department_of_this_store = f"DELETE FROM department WHERE store_id='{store_id}';"
                delete_product_of_this_store = f"DELETE FROM product WHERE store_id='{store_id}';"
                cursor.execute(delete_store)
                cursor.execute(delete_department_of_this_store)
                cursor.execute(delete_product_of_this_store)
                conn.commit()
                cursor.close()
                return {"massege": f"Store with id:{store_id} has been deleted included all its products and departments"}
            else:
                raise StoreExceptionInvalidID("You selected store_id that does not exist")

        
    # create new department
    def create_department(self, name: str , store_id: int):
        with psycopg2.connect(**self.db_params) as conn:
            cursor = conn.cursor()
            IS_STORE_EXIST = f"SELECT EXISTS (SELECT 1 FROM store WHERE store_id = {store_id});"
            cursor.execute(IS_STORE_EXIST)
            is_exist = cursor.fetchone()
            if is_exist[0] == True:
                QUERY = f"INSERT INTO department (department_name, store_id) VALUES ('{name}',{store_id});"

                cursor.execute(QUERY)
                conn.commit()
                cursor.close()
                return {"message": "Department has been created"}
            else:
                raise StoreExceptionInvalidID("You selected store_id that does not exist")
            
    # return all departments
    def get_all_departments(self):
        with psycopg2.connect(**self.db_params) as conn:
            cursor = conn.cursor()
            QUERY = f"SELECT * FROM department;"

            cursor.execute(QUERY)
            result = cursor.fetchall()
            conn.commit()
            cursor.close()
            return result
        
    # return specific department
    def get_specific_department(self, department_id: int):
        with psycopg2.connect(**self.db_params) as conn:
            cursor = conn.cursor()
            IS_DEPARTMENT_EXIST = f"SELECT EXISTS (SELECT 1 FROM department WHERE department_id = {department_id});"
            cursor.execute(IS_DEPARTMENT_EXIST)
            is_department_exist = cursor.fetchone()
            if is_department_exist[0] == True:
                QUERY = f"SELECT * FROM department WHERE department_id = {department_id};"

                cursor.execute(QUERY)
                result = cursor.fetchall()
                conn.commit()
                cursor.close()
                return result
            else:
                raise StoreExceptionInvalidDepartmentID("You selected department_id that does not exist")
    
    # update a department name
    def update_department(self, department_id: int, name: str):
         with psycopg2.connect(**self.db_params) as conn:
                cursor = conn.cursor()
                IS_DEPARTMENT_EXIST = f"SELECT EXISTS (SELECT 1 FROM department WHERE department_id = {department_id});"
                cursor.execute(IS_DEPARTMENT_EXIST)
                is_department_exist = cursor.fetchone()
                if is_department_exist[0] == True:
                    QUERY = f"""UPDATE department
                            SET department_name = '{name}'
                            WHERE department_id = {department_id};"""
                    cursor.execute(QUERY)
                    conn.commit()
                    cursor.close()
                    return {"massege": f"Department name of department id: {department_id} was update"}
                
                else:
                    raise StoreExceptionInvalidDepartmentID("You selected department_id that does not exist")

    # delete a department
    def delete_department(self, department_id: int):
        with psycopg2.connect(**self.db_params) as conn:
            cursor = conn.cursor()
            IS_DEPARTMENT_EXIST = f"SELECT EXISTS (SELECT 1 FROM department WHERE department_id = {department_id});"
            cursor.execute(IS_DEPARTMENT_EXIST)
            is_department_exist = cursor.fetchone()
            if is_department_exist[0] == True:
                delete_department = f"DELETE FROM department WHERE department_id={department_id};"
                delete_products = f"DELETE FROM products WHERE department_id={department_id};"
                cursor.execute(delete_department)
                cursor.execute(delete_products)
                conn.commit()
                cursor.close() 
                return {"massege": f"Department with id:{department_id} has been deleted included all its product"}    
            else:
                raise StoreExceptionInvalidDepartmentID("You selected department_id that does not exist")
    
    # create new product
    def create_product(self, name: str, price: float, quantity: int, specifications: str, department_id: int):
            with psycopg2.connect(**self.db_params) as conn:
                cursor = conn.cursor()
               
                IS_DEPARTMENT_EXIST = f"SELECT EXISTS (SELECT 1 FROM department WHERE department_id = {department_id});"
                cursor.execute(IS_DEPARTMENT_EXIST)
                is_department_exist = cursor.fetchone()
                if is_department_exist[0] == True:
                    find_store_id = f"SELECT store_id FROM department WHERE department_id = {department_id};"
                    cursor.execute(find_store_id)
                    store_id = cursor.fetchone()
                    QUERY = f"INSERT INTO product (product_name, price, quantity, specifications, store_id, department_id) VALUES ('{name}', {price}, {quantity}, '{specifications}', {store_id[0]}, {department_id});"

                    cursor.execute(QUERY)
                    conn.commit()
                    cursor.close()
                    return {"message": "Product has been created"}
                else:
                    raise StoreExceptionInvalidDepartmentID("You selected department_id that does not exist")
                
    # return all the products
    def get_all_products(self):
        with psycopg2.connect(**self.db_params) as conn:
            cursor = conn.cursor()
            QUERY = f"SELECT * FROM product;"

            cursor.execute(QUERY)
            result = cursor.fetchall()
            conn.commit()
            cursor.close()
            return result

    # return a specific product
    def get_specific_product(self, product_id: int):
        with psycopg2.connect(**self.db_params) as conn:
            cursor = conn.cursor()
            IS_PRODUCT_EXIST = f"SELECT EXISTS (SELECT 1 FROM product WHERE product_id = {product_id})"
            cursor.execute(IS_PRODUCT_EXIST)
            is_product_exist = cursor.fetchone()
            if is_product_exist[0] == True:
                QUERY = f"SELECT * FROM product WHERE product_id = {product_id};"

                cursor.execute(QUERY)
                result = cursor.fetchall()
                conn.commit()
                cursor.close()
                return result
            else:
                raise StoreExceptionInvalidProductID("You selected product_id that does not exist")
        
    # update product features
    def update_product(self, product_id:int, name:str, price:float, quantity:int, specifications:str):
        with psycopg2.connect(**self.db_params) as conn:
            cursor = conn.cursor()
            IS_PRODUCT_EXIST = f"SELECT EXISTS (SELECT 1 FROM product WHERE product_id = {product_id})"
            cursor.execute(IS_PRODUCT_EXIST)
            is_product_exist = cursor.fetchone()
            if is_product_exist[0] == True:
                QUERY = f"""UPDATE product
                            SET product_name = '{name}', price = {price}, quantity = {quantity}, specifications = '{specifications}'
                            WHERE product_id = {product_id};"""
                cursor.execute(QUERY)
                conn.commit()
                cursor.close()
                return {"message": f"Product with id:{product_id} has been update"}
            else:
                raise StoreExceptionInvalidProductID("You selected product_id that does not exist")

    # delete a product
    def delete_product(self, product_id):
        with psycopg2.connect(**self.db_params) as conn:
            cursor = conn.cursor()
            IS_PRODUCT_EXIST = f"SELECT EXISTS (SELECT 1 FROM product WHERE product_id = {product_id})"
            cursor.execute(IS_PRODUCT_EXIST)
            is_product_exist = cursor.fetchone()
            if is_product_exist[0] == True:
                QUERY = f"DELETE FROM product WHERE product_id='{product_id}';"
                cursor.execute(QUERY)
                conn.commit()
                cursor.close()
                return {"massege": f"Product with id:{product_id} has been deleted"}
            else:
                raise StoreExceptionInvalidProductID("You selected product_id that does not exist")
    
    # reset the entire system 
    def reset_all(self):
        with psycopg2.connect(**self.db_params) as conn:
            cursor = conn.cursor()
            reset_stores = """DELETE FROM store;"""
            reset_departments = """DELETE FROM department;"""
            reset_products = """DELETE FROM product;"""
            cursor.execute(reset_stores)
            cursor.execute(reset_departments)
            cursor.execute(reset_products)
            reset_store_id = """ALTER SEQUENCE store_store_id_seq RESTART WITH 1;"""
            reset_department_id = """ALTER SEQUENCE department_department_id_seq RESTART WITH 1;"""
            reset_product_id = """ALTER SEQUENCE product_product_id_seq RESTART WITH 1;"""
            cursor.execute(reset_store_id)
            cursor.execute(reset_department_id)
            cursor.execute(reset_product_id)

            conn.commit()
            cursor.close()
            return {"massege": f"Complete a general reset of the entire system"}


    