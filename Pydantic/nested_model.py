from pydantic import BaseModel


class Address(BaseModel):
    street: str
    city: str
    state: str
    pin_code: int


class Employee(BaseModel):
    name: str
    age: int
    gender: str
    salary: int
    address: Address


def get_person_data(emp: Employee):
    print(f"Employee Name: {emp.name}")
    print(f"Age: {emp.age}")
    print(f"Gender: {emp.gender}")
    print(f"Salary: {emp.salary}LPA")
    print(f"Address: {emp.address}")


emp1 = Employee(
    name="Md Ashfak Alam",
    age=28,
    gender="MALE",
    salary=9,
    address=Address(
        street="Lane-8 Arvind Nagar Colony",
        city="Hyderabad",
        state="Telangana",
        pin_code=500008
    )
)

get_person_data(emp1)

# exporting the pydantic object
emp1_dict = emp1.model_dump()
emp1_json = emp1.model_dump_json()
