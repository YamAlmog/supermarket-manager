from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_if_root_is_correct():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

# -------------------------------- Department Testing ---------------------------------
#####################-------------------------------------------#######################

def test_create_and_get_departments():
    new_dep = {"name": "dairy"}
    response = client.post('/departments', json=new_dep)
    assert response.status_code == 200
    assert response.json() == {"message": "Department has been added"}

    response = client.get('/departments')
    assert response.status_code == 200
    assert  response.json() == {"Departments": {"0" : "dairy"}}



def test_create_multiple_departments():
    departments_to_test = [{"name": "dairy"},  {"name": "Electronic"},  {"name": "Vegetables"}]

    for department in departments_to_test:
        post_response = client.post('/departments', json=department)  
        assert post_response.status_code == 200
        assert post_response.json() == {"message": "Department has been added"}

    response = client.get('/departments/2')
    assert response.status_code == 200
    assert  response.json() == {"Department": {"Key": 2, "Value": "Electronic"}}
  

# Negativity test 
def test_department_doesnt_exist():
    response = client.get('/departments/5')
    assert response.status_code == 404
    assert response.json() == {"detail" :"Department not found"}


def test_update_exist_department():
    new_dep = {"name": "deli"}
    response = client.post('/departments', json=new_dep)
    assert response.status_code == 200
    assert response.json() == {"message": "Department has been added"}
    
    update_dep = {"name": "butcher"}
    response = client.put('/departments/0', json=update_dep)
    assert response.status_code == 200
    assert response.json() == {"Department": {"Key": 0, "Value": "butcher"}}

# Negativity test 
def test_update_not_exist_department():
    update_dep = {"name": "butcher"}
    response = client.put('/departments/5', json=update_dep)
    assert response.status_code == 404
    assert response.json() == {"detail" :"Department not found"}


def test_delete_department():
    new_dep = {"name": "dairy"}
    response = client.post('/departments', json=new_dep)
    assert response.status_code == 200
    assert response.json() == {"message": "Department has been added"}
    
    response = client.delete("/departments/0")
    assert response.status_code == 200
    assert response.json() == {"message": f"Department id: {0} has been DELETED!"}

# Negativity test 
def test_delete_not_exist_department():
    response = client.delete("/departments/0")
    assert response.status_code == 404
    assert response.json() == {"detail" :"Department not found"}

# -------------------------------- Product Testing ------------------------------------
#####################-------------------------------------------#######################

def test_create_and_get_product():
    new_dep = {"name": "dairy"}
    response = client.post('/departments', json=new_dep)
    assert response.status_code == 200
    assert response.json() == {"message": "Department has been added"}
    
    new_prod = {
                "name": "Cheese",
                "price": 10.9,
                "quantity": 12,
                "department_id": 0,
                "specifications": "fat 25%"
                }
    response = client.post('/products', json=new_prod)
    assert response.status_code == 200
    assert response.json() == {"message": "Product has been added"}

    response = client.get('/products')
    assert response.status_code == 200
    expected_response = {
                            "Products": {
                                 "0": ["Cheese", 10.9, 12, 0, "fat 25%"]
                            }
                        }
    assert response.json() == expected_response


def test_create_multiple_products():
    new_dep = {"name": "dairy"}
    response = client.post('/departments', json=new_dep)
    assert response.status_code == 200
    assert response.json() == {"message": "Department has been added"}
    
    product_list = [{"name": "Cheese","price": 10.9,"quantity": 12,"department_id": 0,"specifications": "fat 25%"},
                    {"name": "Milk", "price": 7.9, "quantity": 20, "department_id": 0,"specifications": "fat 3%"}]
                        
    for product in product_list:                
        response = client.post('/products', json=product)
        assert response.status_code == 200
        assert response.json() == {"message": "Product has been added"}

    response = client.get('/products/0')
    assert response.status_code == 200
    expected_response = {
                            "Products": {
                                "Key": 0,
                                "Value": ["Cheese", 10.9, 12, 0, "fat 25%"]
                            }
                        }
    assert response.json() == expected_response


# Negativity test 
def test_product_does_not_exist():
    response = client.get('/products/5')
    assert response.status_code == 404
    assert response.json() == {'detail': "Product not found"}


# Negativity test 
def test_product_in_wrong_department_id():
    new_dep = {"name": "cleaning products"}
    response = client.post('/departments', json=new_dep)
    assert response.status_code == 200
    assert response.json() == {"message": "Department has been added"}
    
    new_prod = {
                "name": "dish soap",
                "price": 9.9,
                "quantity": 20,
                "department_id": 2,
                "specifications": "50% Active Ingredient"
                }
    response = client.post('/products', json=new_prod)
    assert response.status_code == 400
    assert response.json() == {"detail": "There is no Department with id:2"}    
        


def test_update_product():
    new_dep = {"name": "cleaning products"}
    dep_response = client.post('/departments', json=new_dep)
    assert dep_response.status_code == 200
    assert dep_response.json() == {"message": "Department has been added"}
    
    new_prod = {
                "name": "dish soap",
                "price": 9.9,
                "quantity": 20,
                "department_id": 0,
                "specifications": "50% Active Ingredient"
                }
    post_response = client.post('/products', json=new_prod)
    assert post_response.status_code == 200
    assert post_response.json() == {"message": "Product has been added"}

    update_prod = {
                    "name": "Bleach",
                    "price": 12.9,
                    "quantity": 20,
                    "department_id": 0,
                    "specifications": "99% Active Ingredient"
                  }
    put_response = client.put('/products/0', json=update_prod)
    assert put_response.status_code == 200
    assert put_response.json() == {"Product": {"Key": 0, "Value": ["Bleach", 12.9, 20, 0, "99% Active Ingredient"]}}
    
    # Negativity testing - put product does not exist
    put_response = client.put('/products/2', json=update_prod)
    assert put_response.status_code == 404
    assert put_response.json() == {"detail": "Product not found"}

    # Negativity testing - put in department does not exist
    update_wrong_prod = {
                        "name": "Bleach",
                        "price": 12.9,
                        "quantity": 20,
                        "department_id": 3,
                        "specifications": "99% Active Ingredient"
                    }
    response = client.put('/products/0', json=update_wrong_prod)
    assert response.status_code == 400
    assert response.json() == {"detail": "There is no Department with id:3"}



def test_delete_product():
    new_dep = {"name": "cleaning products"}
    response = client.post('/departments', json=new_dep)
    assert response.status_code == 200
    assert response.json() == {"message": "Department has been added"}
    
    new_prod = {
                "name": "dish soap",
                "price": 9.9,
                "quantity": 20,
                "department_id": 0,
                "specifications": "50% Active Ingredient"
                }
    response = client.post('/products', json=new_prod)
    assert response.status_code == 200
    assert response.json() == {"message": "Product has been added"}

    delete_response = client.delete('/products/0')
    assert delete_response.status_code == 200
    assert delete_response.json() == {"message": "Products id: 0 has been DELETED!"}

    # Negativity testing - delete product does not exist
    delete_response = client.delete('/products/5')
    assert delete_response.status_code == 404
    assert delete_response.json() == {"detail" : "Product not found"}