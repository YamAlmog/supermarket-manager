import psycopg2

# Replace these values with your PostgreSQL connection details
db_params = {
    'host': 'localhost',
    'port': 5432,
    'database': 'Learning',
    'user': 'postgres',
    'password': '123456',
}

# Connect to the PostgreSQL database
conn = psycopg2.connect(**db_params)

# Create a cursor
cursor = conn.cursor()

# Define the SQL statement to create a table
create_store_table_query = """
    CREATE TABLE Store (
        store_id SERIAL PRIMARY KEY,
        store_name VARCHAR(100)
    )
"""
create_department_table_query = """
    CREATE TABLE Department (
        department_id SERIAL PRIMARY KEY,
        department_name VARCHAR(100),
        store_id INT
    )
"""
create_product_table_query = """
    CREATE TABLE Product (
        product_id SERIAL PRIMARY KEY,
        product_name VARCHAR(100),
        store_id INT,
        department_id INT
    )
"""


# Execute the SQL statement
cursor.execute(create_store_table_query)
cursor.execute(create_department_table_query)
cursor.execute(create_product_table_query)


# add_values_to_department="""INSERT INTO Department (department_name, store_id)
#                             VALUES ({},{});""".format("HR",1)
                                
# cursor.execute(add_values_to_department)


# Commit the changes
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()
