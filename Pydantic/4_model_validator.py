from pydantic import BaseModel, EmailStr, model_validator
from typing import List, Dict, Optional


class Patient(BaseModel):
    name: str
    email: EmailStr
    age: int
    weight: float
    is_married: Optional[bool] = False
    allergies: Optional[List[str]] = None
    contact_details: Dict[str, str]

    # model validation
    @model_validator(mode='after')
    def is_emergency_number(self):
        if self.age > 60 and 'emergency_contact' not in self.contact_details:
            raise ValueError("Patients older than 60 must have emergency contact number")
        if len(self.contact_details['emergency_contact']) < 10:
            raise ValueError("Patient should have a valid contact number")
        return self


def insert_patient_data(patient: Patient):
    print(f"Patient Name: {patient.name}")
    print(f"Email: {patient.email}")
    print(f"Age: {patient.age}")
    print(f"Weight: {patient.weight}")
    print(f"Is_Married: {patient.is_married}")
    print(f"Allergies: {patient.allergies}")
    print(f"Contact Details: {patient.contact_details}")
    print("Patient record inserted successfully")


patient1 = Patient(
    name="Bruce Wayne",
    email="Brucewayne2002@gmail.com",
    age=78,
    weight=89.74,
    contact_details={
        "contact": "9012345678",
        "address": "Batman tower, Washington (America)",
        "emergency_contact": "9912345679"
    }
)

insert_patient_data(patient1)
