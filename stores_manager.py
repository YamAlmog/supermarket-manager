
import psycopg2
from Error import StoreExceptionInvalidID, StoreException, StoreExceptionInvalidDepartmentID, StoreExceptionInvalidProductID
from models import ProductDetails, DepartmentDetails, Store, StoreDetails

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
    def create_store(self, name: str) -> str:
        with psycopg2.connect(**self.db_params) as conn:
            cursor = conn.cursor()
            QUERY = f"INSERT INTO store (store_name) VALUES ('{name}')"

            cursor.execute(QUERY)
            conn.commit()
            cursor.close()
            return "Store has been created"

    # return all stores
    def get_all_stores(self) -> list:
        with psycopg2.connect(**self.db_params) as conn:
            cursor = conn.cursor()
            QUERY = f"Select * from store"
            cursor.execute(QUERY)
            results = cursor.fetchall()
            all_store_details = []
            for row in results:
                store_details= Store(store_id=row[0], store_name=row[1])
                all_store_details.append(store_details)
            cursor.close()
            return all_store_details
        
    # delete specific store included its department and product
    def delete_store(self, store_id: int) -> str:
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
                return f"Store with id:{store_id} has been deleted included all its products and departments"
            else:
                raise StoreExceptionInvalidID("You selected store_id that does not exist")

        
    # create new department
    def create_department(self, name: str , store_id: int) -> str:
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
                return "Department has been added"
            else:
                raise StoreExceptionInvalidID("You selected store_id that does not exist")
            
    # return all departments
    def get_all_departments(self) -> list:
        with psycopg2.connect(**self.db_params) as conn:
            cursor = conn.cursor()
            QUERY = f"SELECT * FROM department;"

            cursor.execute(QUERY)
            result = cursor.fetchall()
            all_department_details = []
            for row in result:
                department_details= DepartmentDetails(department_id=row[0], department_name=row[1], store_id=row[2])
                all_department_details.append(department_details)
            
            conn.commit()
            cursor.close()
            return all_department_details
        
    # return specific department
    def get_specific_department(self, department_id: int) -> DepartmentDetails:
        with psycopg2.connect(**self.db_params) as conn:
            cursor = conn.cursor()
            IS_DEPARTMENT_EXIST = f"SELECT EXISTS (SELECT 1 FROM department WHERE department_id = {department_id});"
            cursor.execute(IS_DEPARTMENT_EXIST)
            is_department_exist = cursor.fetchone()
            if is_department_exist[0] == True:
                QUERY = f"SELECT * FROM department WHERE department_id = {department_id};"

                cursor.execute(QUERY)
                row = cursor.fetchone()
                department_details= DepartmentDetails(department_id=row[0], department_name=row[1], store_id=row[2])
                conn.commit()
                cursor.close()
                return department_details
            else:
                raise StoreExceptionInvalidDepartmentID("You selected department_id that does not exist")
    
    # update a department name
    def update_department(self, department_id: int, name: str) -> str:
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
                    return f"Department name of department id: {department_id} was update"
                
                else:
                    raise StoreExceptionInvalidDepartmentID("You selected department_id that does not exist")

    # delete a department
    def delete_department(self, department_id: int) -> str:
        with psycopg2.connect(**self.db_params) as conn:
            cursor = conn.cursor()
            IS_DEPARTMENT_EXIST = f"SELECT EXISTS (SELECT 1 FROM department WHERE department_id = {department_id});"
            cursor.execute(IS_DEPARTMENT_EXIST)
            is_department_exist = cursor.fetchone()
            if is_department_exist[0] == True:
                delete_department = f"DELETE FROM department WHERE department_id={department_id};"
                delete_products = f"DELETE FROM product WHERE department_id={department_id};"
                cursor.execute(delete_department)
                cursor.execute(delete_products)
                conn.commit()
                cursor.close() 
                return f"Department with id:{department_id} has been deleted included all its product"   
            else:
                raise StoreExceptionInvalidDepartmentID("You selected department_id that does not exist")
    
    # create new product
    def create_product(self, name: str, price: float, quantity: int, specifications: str, department_id: int) -> str:
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
                    return "Product has been added"
                else:
                    raise StoreExceptionInvalidDepartmentID("You selected department_id that does not exist")
                
    # return all the products
    def get_all_products(self):
        with psycopg2.connect(**self.db_params) as conn:
            cursor = conn.cursor()
            QUERY = f"SELECT * FROM product;"

            cursor.execute(QUERY)
            result = cursor.fetchall()
            
            products_by_store = []
            store_details = StoreDetails
            """
            { 
                store_id : 1 
                store_name : "my_store"
                products : [products_list_for_store]
            }
            """
            for row in result:
                products_list_for_store = []
                               
                product_details = ProductDetails(product_id=row[0], product_name=row[1], department_id=row[3], price=row[4], quantity=row[5], specifications=row[6])
                
                store_id = row[2]
                # insert product into store_details dict so the key is store_id(row[2]) and value is list of products
                store_exists = any(store["store_id"] == store_id for store in products_by_store)
                
                # if store_details have store with id=row[0]- insert the new product to it
                if store_exists:
                    products_list_for_store #should be products list of store_details
                    products_list_for_store.append(product_details) #add the new product_details to product list
                    # update the product list of store_details 
                
                # else we would like to create new store detail and insert first product to it
                else:
                    
                    products_list_for_store.append(product_details)
                    store_details = StoreDetails(store_id=store_id, store_name='none', products=products_list_for_store)

            conn.commit()
            cursor.close()
            return products_by_store

    # return a specific product
    def get_specific_product(self, product_id: int) -> ProductDetails:
        with psycopg2.connect(**self.db_params) as conn:
            cursor = conn.cursor()
            IS_PRODUCT_EXIST = f"SELECT EXISTS (SELECT 1 FROM product WHERE product_id = {product_id})"
            cursor.execute(IS_PRODUCT_EXIST)
            is_product_exist = cursor.fetchone()
            if is_product_exist[0] == True:
                QUERY = f"SELECT * FROM product WHERE product_id = {product_id};"

                cursor.execute(QUERY)
                row = cursor.fetchone()
                product_details = ProductDetails(product_id=row[0], product_name=row[1], store_id=row[2], department_id=row[3], price=row[4], quantity=row[5], specifications=row[6])
                conn.commit()
                cursor.close()
                return product_details
            else:
                raise StoreExceptionInvalidProductID("You selected product_id that does not exist")
        
    # update product features
    def update_product(self, product_id:int, name:str, price:float, quantity:int, specifications:str) -> str:
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
                return f"Product with id:{product_id} has been update"
            else:
                raise StoreExceptionInvalidProductID("You selected product_id that does not exist")

    # delete a product
    def delete_product(self, product_id) -> str:
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
                return f"Product with id:{product_id} has been deleted"
            else:
                raise StoreExceptionInvalidProductID("You selected product_id that does not exist")
    
    # reset the entire system 
    def reset_all(self) -> str:
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
            return "Complete a general reset of the entire system"


    