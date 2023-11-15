from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_if_root_is_correct():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_get_departments():
    response = client.get('/departments')
    assert response.status_code == 200
    assert "Departments" in response.json()

def test_create_department():
    new_dep = {"name": "dairy"}
    response = client.post('/departments', json=new_dep)
    assert response.status_code == 200
    assert response.json() == {"message": "Department has been added"}

def test_get_specific_department():
    response = client.get('/departments/0')
    assert response.status_code == 200
    assert response.json()["Department"]["Key"] == 0
    assert response.json()["Department"]["Value"] == "dairy"


def test_update_department():
    update_dep = {"name": "deli"}
    response = client.put('/departments/0', json=update_dep)
    assert response.status_code == 200
    assert response.json() == {"Department": {"Key": 0, "Value": "deli"}}


def test_delete_department():
    response = client.delete("/departments/0")
    assert response.status_code == 200
    assert response.json() == {"message": f"Department id: {0} has been DELETED!"}

'''def test_get_specific_department():
    response = client.get(f"/departments/{0}")
    assert response.status_code == 200
    assert response.json()["Department"]["Key"] == 0
    assert response.json()["Department"]["Value"] == "dairy"'''


def test_create_department():
    new_dep = {"name": "dairy"}
    response = client.post('/departments', json=new_dep)
    assert response.status_code == 200
    assert response.json() == {"message": "Department has been added"}

def test_get_products():
    response = client.get('/products')
    assert response.status_code == 200
    assert "Products" in response.json()


def test_create_product():
    new_prod = {
                "name": "Cheese",
                "price": 10.9,
                "quantity": 12,
                "department_id": 1,
                "specifications": "fat 25%"
                }
    response = client.post('/products', json=new_prod)
    assert response.status_code == 200
    assert response.json() == {"message": "Product has been added"}

def test_get_specific_product():
    response = client.get('/products/0')
    assert response.status_code == 200
    expected_response = {
                            "Products": {
                                "Key": 1,
                                "Value": ["Cheese", 10.9, 12, 1, "fat 25%"]
                            }
                        }
   
    assert response.json() == expected_response
    #assert response.json()["Products"]["Key"] == 0
        
        

def test_update_product():
    pass 

def test_delete_product():
    pass 
