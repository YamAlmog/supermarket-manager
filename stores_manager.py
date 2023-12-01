
import psycopg2
from Error import StoreExceptionInvalidID, StoreException, StoreExceptionInvalidDepartmentID


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
    def create_store(self, name: str) -> int:
        with psycopg2.connect(**self.db_params) as conn:
            cursor = conn.cursor()
            QUERY = f"INSERT INTO store (store_name) VALUES ('{name}')"

            cursor.execute(QUERY)
            conn.commit()
            cursor.close()

    def get_all_stores(self):
        with psycopg2.connect(**self.db_params) as conn:
            cursor = conn.cursor()
            QUERY = f"Select * from store"

            cursor.execute(QUERY)
            results = cursor.fetchall()

            # Print the results
            for row in results:
                print(f"row: {row}")

            cursor.close()

            return results
        
    def delete_store(self, name: str) :
        with psycopg2.connect(**self.db_params) as conn:
            cursor = conn.cursor()
            QUERY = f"DELETE FROM store WHERE store_name='{name}';"

            cursor.execute(QUERY)
            conn.commit()
            cursor.close()

            
        

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
                return {"message": "Department has been added"}
            else:
                raise StoreExceptionInvalidID("You select store_id that does not exist")
            

    def get_all_departments(self, store_id: int):
        with psycopg2.connect(**self.db_params) as conn:
            cursor = conn.cursor()
            IS_STORE_EXIST = f"SELECT EXISTS (SELECT 1 FROM store WHERE store_id = {store_id});"
            cursor.execute(IS_STORE_EXIST)
            is_exist = cursor.fetchone()
            if is_exist[0] == True:
                QUERY = f"SELECT * FROM department WHERE store_id={store_id};"

                cursor.execute(QUERY)
                result = cursor.fetchall()
                conn.commit()
                cursor.close()
                return result
            else:
                raise StoreExceptionInvalidID("You select store_id that does not exist")

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
                raise StoreExceptionInvalidDepartmentID("You select department_id that does not exist")
            

    def create_product(self, name: str , store_id: int, department_id: int):
            pass
    
    def update_product(self, product_id, department_id, store_id):
        pass

    