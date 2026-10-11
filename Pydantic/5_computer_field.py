from typing import Optional, List, Dict
from pydantic import BaseModel, EmailStr, computed_field


class Patient(BaseModel):
    name: str
    email: EmailStr
    age: int
    weight: float
    height: float
    is_married: Optional[bool] = False
    allergies: Optional[List[str]] = None
    contact_details: Dict[str, str]

    @computed_field
    @property
    def bmi(self) -> float:
        return round((self.weight / (self.height ** 2)), 2)

def insert_patient_data(patient: Patient):
    print(f"Patient Name: {patient.name}")
    print(f"Email: {patient.email}")
    print(f"Age: {patient.age}")
    print(f"Weight: {patient.weight}")
    print(f"Height: {patient.height}")
    print(f"BMI: {patient.bmi}")
    print(f"Is_Married: {patient.is_married}")
    print(f"Allergies: {patient.allergies}")
    print(f"Contact Details: {patient.contact_details}")
    print("Patient record inserted successfully")


patient1 = Patient(
    name="Bruce Wayne",
    email="Brucewayne2002@gmail.com",
    age=78,
    weight=89.74,
    height=1.74,
    contact_details={
        "contact": "9012345678",
        "address": "Batman tower, Washington (America)",
        "emergency_contact": "9912345679"
    }
)

insert_patient_data(patient1)
