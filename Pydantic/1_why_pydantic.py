def insert_patient_data(name: str, age: int):
    if type(name) == str and type(age) == int:
        if age < 0:
            raise ValueError("age cannot be negative")
        print(name)
        print(age)
        print("Record inserted successfully")
    else:
        raise TypeError("Invalid data type")


def update_patient_data(name: str, age: int):
    if type(name) == str and type(age) == int:
        if age < 0:
            raise ValueError("age cannot be negative")
        print(name)
        print(age)
        print("Record inserted successfully")
    else:
        raise TypeError("Invalid data type")


insert_patient_data("Ruhi Sharma", 23)
# insert_patient_data("Ruhi Sharma", 'twenty-three')
update_patient_data("Ruhi Sharma", 32)
# update_patient_data("Ruhi Sharma", -26)

# There are three problems:

# 1:  Repeated validation: You write the same validation logic in both insert_patient_data() and update_patient_data().

# 2:  Type hints don't enforce types: Writing name: str and age: int does not automatically reject invalid values in Python.

# 3:  Limited validation: Your code checks only data types. It doesn't check whether the name is empty or the age is within a reasonable range.
