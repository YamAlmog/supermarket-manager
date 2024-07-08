from fastapi.testclient import TestClient
from main import app
import warnings

# Filter out DeprecationWarning from httpx
warnings.filterwarnings("ignore", category=DeprecationWarning, module="httpx")

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

# ----------------------------------- Store Testing -----------------------------------
#####################-------------------------------------------#######################

@setup_test_decorator
def test_new_store():
    response = client.post("/create_store", params={"name": "Store"})
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
    assert  response.json() == {"Departments": {
                                                "1": {
                                                "store_id": 1,
                                                "store_name": "MyStore",
                                                "departments": 
                                                        [{"department_name": "dairy",
                                                        "department_id": 1,
                                                        "store_id": 1}]
                                }}}
                                                                                                                                

@setup_test_decorator
def test_create_multiple_departments():
    departments_to_test = [{"department_name": "dairy"},  {"department_name": "Electronic"},  {"department_name": "Vegetables"}]

    for department in departments_to_test:
        post_response = client.post('/departments', json=department, params={"store_id": 1})  
        assert post_response.status_code == 200
        assert post_response.json() == {"message": "Department has been added"}

    response = client.get('/departments')
    assert response.status_code == 200
    assert  response.json() == {
                                "Departments": {
                                    "1": {
                                    "store_id": 1,
                                    "store_name": "MyStore",
                                    "departments": [
                                        {
                                        "department_name": "dairy",
                                        "department_id": 1,
                                        "store_id": 1
                                        },
                                        {
                                        "department_name": "Electronic",
                                        "department_id": 2,
                                        "store_id": 1
                                        },
                                        {
                                        "department_name": "Vegetables",
                                        "department_id": 3,
                                        "store_id": 1
                                        }
                                    ]
                                    }
                                }
                                }

# Negativity test 
@setup_test_decorator
def test_department_doesnt_exist():
    response = client.get('/specific_department' , params={"department_id": 5})
    assert response.status_code == 404
    assert response.json() == {"detail" :"You selected department_id that does not exist"}


@setup_test_decorator
def test_update_exist_department():
    new_dep = {"department_name": "deli"}
    response = client.post('/departments', json=new_dep, params={"store_id": 1})
    assert response.status_code == 200
    assert response.json() == {"message": "Department has been added"}
    
    update_dep = {"department_name": "butcher"}
    response = client.put('/departments', json=update_dep, params={"department_id": 1})
    assert response.status_code == 200
    assert response.json() == {"message": "Department name of department id: 1 was update"}

# Negativity test 
@setup_test_decorator
def test_update_not_exist_department():
    update_dep = {"department_name": "butcher"}
    response = client.put('/departments', json=update_dep, params={"department_id": 1})
    assert response.status_code == 404
    assert response.json() == {"detail" :"You selected department_id that does not exist"}

@setup_test_decorator
def test_delete_department():
    new_dep = {"department_name": "dairy"}
    response = client.post('/departments', json=new_dep, params={"store_id": 1})
    assert response.status_code == 200
    assert response.json() == {"message": "Department has been added"}
    
    response = client.delete("/departments", params={"department_id": 1})
    assert response.status_code == 200
    assert response.json() == {"message": "Department with id:1 has been deleted included all its product"}

# Negativity test 
@setup_test_decorator
def test_delete_not_exist_department():
    response = client.delete("/departments", params={"department_id": 1})
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


    get_response = client.get('/specific_product', params={"product_id": 1})
    assert get_response.status_code == 200
    expected_response = {
                        "product_name": "Cheese",
                        "price": 10.9,
                        "quantity": 12,
                        "specifications": "fat 25%",
                        "product_id": 1,
                        "department_id": 1
                        }
    assert get_response.json() == expected_response


@setup_test_decorator
def test_create_multiple_products():
    new_dep = {"department_name": "dairy"}
    response = client.post('/departments', json=new_dep, params={"store_id": 1})
    assert response.status_code == 200
    assert response.json() == {"message": "Department has been added"}
    
    product_list = [{"product_name": "Blue cheese", "price": 10.9,"quantity": 12,"department_id": 1,"specifications": "fat 25%"},
                    {"product_name": "Milk", "price": 7.9, "quantity": 20, "department_id": 1,"specifications": "fat 3%"}]
                        
    for product in product_list:                
        response = client.post('/products', json=product, params={"department_id": 1})
        assert response.status_code == 200
        assert response.json() == {"message": "Product has been added"}

    response = client.get('/products', params={"store_id": 0})
    assert response.status_code == 200
    expected_response = {
                            "All Products": {
                            "1": {
                            "store_id": 1,
                            "store_name": "MyStore",
                            "products": [
                                {
                                "product_name": "Blue cheese",
                                "price": 10.9,
                                "quantity": 12,
                                "specifications": "fat 25%",
                                "product_id": 1,
                                "department_id": 1
                                },
                                {
                                "product_name": "Milk",
                                "price": 7.9,
                                "quantity": 20,
                                "specifications": "fat 3%",
                                "product_id": 2,
                                "department_id": 1
                                }
                            ]
                            }
                            }
                        }
    assert response.json() == expected_response


# Negativity test 
@setup_test_decorator
def test_product_does_not_exist():
    response = client.get('/specific_product', params={"product_id": 5})
    assert response.status_code == 404
    assert response.json() == {'detail': "You selected product_id that does not exist"}


# Negativity test 
@setup_test_decorator
def test_product_in_wrong_department_id():
    new_dep = {"department_name": "cleaning products"}
    response = client.post('/departments', json=new_dep, params={"store_id": 1})
    assert response.status_code == 200
    assert response.json() == {"message": "Department has been added"}
    
    new_prod = {
                "product_name": "dish soap",
                "price": 9.9,
                "quantity": 20,
                "specifications": "50% Active Ingredient"
                }
    response = client.post('/products', json=new_prod, params={"department_id": 2})
    assert response.status_code == 404
    assert response.json() == {"detail": "You selected department_id that does not exist"}    
        

@setup_test_decorator
def test_update_product():
    new_dep = {"department_name": "cleaning products"}
    dep_response = client.post('/departments', json=new_dep, params={"store_id": 1})
    assert dep_response.status_code == 200
    assert dep_response.json() == {"message": "Department has been added"}
    
    new_prod = {
                "product_name": "dish soap",
                "price": 9.9,
                "quantity": 20,
                "specifications": "50% Active Ingredient"
                }
    post_response = client.post('/products', json=new_prod, params={"department_id": 1})
    assert post_response.status_code == 200
    assert post_response.json() == {"message": "Product has been added"}

    update_prod = {
                    "product_name": "Bleach",
                    "price": 12.9,
                    "quantity": 20,
                    "specifications": "99% Active Ingredient"
                  }
    put_response = client.put('/products', json=update_prod, params={"product_id": 1})
    assert put_response.status_code == 200
    assert put_response.json() == {"message": "Product with id:1 has been update"}
    
    # Negativity testing - put product does not exist
    put_response = client.put('/products', json=update_prod, params={"product_id": 5})
    assert put_response.status_code == 404
    assert put_response.json() == {"detail": "You selected product_id that does not exist"}



@setup_test_decorator
def test_delete_product():
    new_dep = {"department_name": "cleaning products"}
    response = client.post('/departments', json=new_dep, params={"store_id": 1})
    assert response.status_code == 200
    assert response.json() == {"message": "Department has been added"}
    
    new_prod = {
                "product_name": "dish soap",
                "price": 9.9,
                "quantity": 20,
                "specifications": "50% Active Ingredient"
                }
    post_response = client.post('/products', json=new_prod, params={"department_id": 1})
    assert post_response.status_code == 200
    assert post_response.json() == {"message": "Product has been added"}

    delete_response = client.delete('/products', params={"product_id": 1})
    assert delete_response.status_code == 200
    assert delete_response.json() == {"message": "Product with id:1 has been deleted"}

    # Negativity testing - delete product does not exist
    delete_response = client.delete('/products', params={"product_id": 5})
    assert delete_response.status_code == 404
    assert delete_response.json() == {"detail" : "You selected product_id that does not exist"}