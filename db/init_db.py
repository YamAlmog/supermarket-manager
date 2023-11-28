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
create_table_query = """
    CREATE TABLE ExampleTable4 (
        id serial PRIMARY KEY,
        name VARCHAR(100),
        age INT
    )
"""

# Execute the SQL statement
cursor.execute(create_table_query)
# Commit the changes
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()
