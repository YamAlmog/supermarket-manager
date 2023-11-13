from fastapi import FastAPI
from models import Department, Product

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


departments = []

# Get all departments
@app.get("/departments")
async def get_departments():
    return {"Departments": departments}

# Get single department
@app.get("/departments/{department_id}")
async def get_department(department_id: int):
    for department in departments:
        if department.id == department_id:
            return {"Department": department}
    return {"message": f"Department with id:{department_id} not found"}


# Create a department
@app.post("/departments")
async def create_department(department: Department):
    departments.append(department)
    return {"message": "Department has been added"}

# Update a department
@app.put("/departments/{department_id}")
async def update_department(department_id: int, department_obj: Department):
    for department in departments:
        if department.id == department_id:
            department.name = department_obj.name
            return {"Department": department}
    return {"message": "No departments found to update"}

# Delete a department
@app.delete("/departments/{department_id}")
async def delete_department(department_id: int):
    for department in departments:
        if department.id == department_id:
            departments.remove(department)
            return {"message": "Department has been DELETED!"}
    return {"message": f"Department with id:{department_id} not found"}

