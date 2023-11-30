
import psycopg2



class StoresManager:

    def __init__(self):
        # Initialize db connections 
        # Replace these values with your PostgreSQL connection details
        self.db_params = {
            'host': 'localhost',
            'port': 5432,
            'database': 'Learning',
            'user': 'postgres',
            'password': '123456',
        }

            

    # create new store. return store id
    def create_store(self, name :str) -> int:
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
        
    

    def create_department(self, name :str , store_id :str) -> int:
        pass

    def update_product(self, product_id, department_id, store_id):
        pass

    