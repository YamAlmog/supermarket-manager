from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def setup_test_decorator(original_func):
    def wrapper_function(*args):
        print("Clear all stores data")
        client.delete("/")

        # create new store at id 1
        response = client.post("/create_store", params={"name": "MyStore"})
        assert response.status_code == 200
        print("Created a new store")


        # call the original function 
        return original_func(*args)
        
    return wrapper_function





@setup_test_decorator
def test_new_store():
    response = client.post("/create_store", params={"name": "MyStore"})
    assert response.status_code == 200

@setup_test_decorator
def test_if_root_is_correct():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to store API"}

@setup_test_decorator
def test_if_clean_function_works():
    response = client.delete('/')
    assert response.status_code == 200
    assert response.json() == {"message": "Complete a general reset of the entire system"}


# -------------------------------- Department Testing ---------------------------------
#####################-------------------------------------------#######################

@setup_test_decorator
def test_create_and_get_departments():
    new_dep = {"department_name": "dairy"}
    response = client.post('/departments', json=new_dep, params={"store_id": 1})
    assert response.status_code == 200
    assert response.json() == {"message": "Department has been added"}

    response = client.get('/departments')
    assert response.status_code == 200
    assert  response.json() == {"Departments": [{'department_id': 1, 'department_name': 'dairy', 'store_id': 1}]}



@setup_test_decorator
def test_create_multiple_departments():
    departments_to_test = [{"department_name": "dairy"},  {"department_name": "Electronic"},  {"department_name": "Vegetables"}]

    for department in departments_to_test:
        post_response = client.post('/departments', json=department, params={"store_id": 1})  
        assert post_response.status_code == 200
        assert post_response.json() == {"message": "Department has been added"}

    response = client.get('/departments/1' , params={"store_id": 1})
    assert response.status_code == 200
    assert  response.json() == {'department_id': 1, 'department_name': 'dairy', 'store_id': 1}
  

# Negativity test 
@setup_test_decorator
def test_department_doesnt_exist():
    response = client.get('/departments/5' , params={"store_id": 1})
    assert response.status_code == 404
    assert response.json() == {"detail" :"You selected department_id that does not exist"}


@setup_test_decorator
def test_update_exist_department():
    new_dep = {"department_name": "deli"}
    response = client.post('/departments', json=new_dep, params={"store_id": 1})
    assert response.status_code == 200
    assert response.json() == {"message": "Department has been added"}
    
    update_dep = {"department_name": "butcher"}
    response = client.put('/departments/1', json=update_dep, params={"store_id": 1})
    assert response.status_code == 200
    assert response.json() == {"message": "Department name of department id: 1 was update"}

# Negativity test 
@setup_test_decorator
def test_update_not_exist_department():
    update_dep = {"department_name": "butcher"}
    response = client.put('/departments/0', json=update_dep, params={"store_id": 0})
    assert response.status_code == 404
    assert response.json() == {"detail" :"You selected department_id that does not exist"}

@setup_test_decorator
def test_delete_department():
    new_dep = {"department_name": "dairy"}
    response = client.post('/departments', json=new_dep, params={"store_id": 1})
    assert response.status_code == 200
    assert response.json() == {"message": "Department has been added"}
    
    response = client.delete("/departments/1")
    assert response.status_code == 200
    assert response.json() == {"message": "Department with id:1 has been deleted included all its product"}

# Negativity test 
@setup_test_decorator
def test_delete_not_exist_department():
    response = client.delete("/departments/2")
    assert response.status_code == 404
    assert response.json() == {"detail" :"You selected department_id that does not exist"}

# -------------------------------- Product Testing ------------------------------------
#####################-------------------------------------------#######################

@setup_test_decorator
def test_create_and_get_product():
    new_dep = {"department_name": "dairy"}
    post_response = client.post('/departments', json=new_dep, params={"store_id": 1})
    assert post_response.status_code == 200
    assert post_response.json() == {"message": "Department has been added"}
    
    new_prod = {
                "product_name": "Cheese",
                "price": 10.9,
                "quantity": 12,
                "specifications": "fat 25%"
                }
    response = client.post('/products', json=new_prod, params={"department_id": 1})
    assert response.status_code == 200
    assert response.json() == {"message": "Product has been added"}

    get_response = client.get('/products')
    assert get_response.status_code == 200
    expected_response = {
                            "Products": {
                                "product_name": "Cheese",
                                "price": 10.9,
                                "quantity": 12,
                                "specifications": "fat 25%"
                            }
                        }
    assert get_response.json() == expected_response


@setup_test_decorator
def test_create_multiple_products():
    new_dep = {"name": "dairy"}
    response = client.post('/departments', json=new_dep, params={"store_id": 0})
    assert response.status_code == 200
    assert response.json() == {"message": "Department has been added"}
    
    product_list = [{"name": "Blue cheese","price": 10.9,"quantity": 12,"department_id": 0,"specifications": "fat 25%"},
                    {"name": "Milk", "price": 7.9, "quantity": 20, "department_id": 0,"specifications": "fat 3%"}]
                        
    for product in product_list:                
        response = client.post('/products', json=product, params={"store_id": 0})
        assert response.status_code == 200
        assert response.json() == {"message": "Product has been added"}

    response = client.get('/products/0', params={"store_id": 0})
    assert response.status_code == 200
    expected_response = {
                            "Products": {
                                "Key": 0,
                                "Value": ["Blue cheese", 10.9, 12, 0, "fat 25%"]
                            }
                        }
    assert response.json() == expected_response


# Negativity test 
@setup_test_decorator
def test_product_does_not_exist():
    response = client.get('/products/5', params={"store_id": 0})
    assert response.status_code == 404
    assert response.json() == {'detail': "Product not found"}


# Negativity test 
@setup_test_decorator
def test_product_in_wrong_department_id():
    new_dep = {"name": "cleaning products"}
    response = client.post('/departments', json=new_dep, params={"store_id": 0})
    assert response.status_code == 200
    assert response.json() == {"message": "Department has been added"}
    
    new_prod = {
                "name": "dish soap",
                "price": 9.9,
                "quantity": 20,
                "department_id": 2,
                "specifications": "50% Active Ingredient"
                }
    response = client.post('/products', json=new_prod, params={"store_id": 0})
    assert response.status_code == 400
    assert response.json() == {"detail": "There is no Department with id:2"}    
        

@setup_test_decorator
def test_update_product():
    new_dep = {"name": "cleaning products"}
    dep_response = client.post('/departments', json=new_dep, params={"store_id": 0})
    assert dep_response.status_code == 200
    assert dep_response.json() == {"message": "Department has been added"}
    
    new_prod = {
                "name": "dish soap",
                "price": 9.9,
                "quantity": 20,
                "department_id": 0,
                "specifications": "50% Active Ingredient"
                }
    post_response = client.post('/products', json=new_prod, params={"store_id": 0})
    assert post_response.status_code == 200
    assert post_response.json() == {"message": "Product has been added"}

    update_prod = {
                    "name": "Bleach",
                    "price": 12.9,
                    "quantity": 20,
                    "department_id": 0,
                    "specifications": "99% Active Ingredient"
                  }
    put_response = client.put('/products/0', json=update_prod, params={"store_id": 0})
    assert put_response.status_code == 200
    assert put_response.json() == {"Product": {"Key": 0, "Value": ["Bleach", 12.9, 20, 0, "99% Active Ingredient"]}}
    
    # Negativity testing - put product does not exist
    put_response = client.put('/products/2', json=update_prod, params={"store_id": 0})
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
    response = client.put('/products/0', json=update_wrong_prod, params={"store_id": 0})
    assert response.status_code == 400
    assert response.json() == {"detail": "There is no Department with id:3"}



@setup_test_decorator
def test_delete_product():

    new_dep = {"name": "cleaning products"}
    response = client.post('/departments', json=new_dep, params={"store_id": 0})
    assert response.status_code == 200
    assert response.json() == {"message": "Department has been added"}
    
    new_prod = {
                "name": "dish soap",
                "price": 9.9,
                "quantity": 20,
                "department_id": 0,
                "specifications": "50% Active Ingredient"
                }
    response = client.post('/products', json=new_prod, params={"store_id": 0})
    assert response.status_code == 200
    assert response.json() == {"message": "Product has been added"}

    delete_response = client.delete('/products/0', params={"store_id": 0})
    assert delete_response.status_code == 200
    assert delete_response.json() == {"message": "Products id: 0 has been DELETED!"}

    # Negativity testing - delete product does not exist
    delete_response = client.delete('/products/5', params={"store_id": 0})
    assert delete_response.status_code == 404
    assert delete_response.json() == {"detail" : "Product not found"}