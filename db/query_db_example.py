import psycopg2

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

# Execute a query
cursor.execute("SELECT * FROM students")
def insert_new_department(name:str, store_id:int):       
    cursor.execute('''INSERT INTO department (department_name, store_id)
                    VALUES ('{}', {});'''.format(name,store_id))


insert_new_department("HR", 2)
conn.commit()
# Fetch all the results
#results = cursor.fetchall()
cursor.fetchall()
'''# Print the results
for row in results:
    print(row)
'''
# Close the cursor and connection
cursor.close()
conn.close()