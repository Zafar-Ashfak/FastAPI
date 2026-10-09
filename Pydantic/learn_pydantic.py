from pydantic import BaseModel, EmailStr, AnyUrl
from typing import List, Dict, Optional

class Patient(BaseModel):
    name : str # required
    email : EmailStr # Validate
    age : int # required
    weight : float# required
    is_married : bool = False # Default value
    allergies : Optional[List[str]] = None # Optional List with default
    contact_details : Dict[str, str] # required Dict
    linked_url : Optional[AnyUrl] = None

def insert_patient_data(patient : Patient):
    print(f"Patient Name: {patient.name}")
    print(f"Email: {patient.email}")
    print(f"Age: {patient.age}")
    print(f"Weight: {patient.weight}")
    print(f"Is Married: {patient.is_married}")
    print(f"Allergies: {patient.allergies}")
    print(f"Contact Details: {patient.contact_details}")
    print(f"Contact Details: {patient.linked_url}")
    print("Record inserted successfully!")
    print()

patient1 = Patient(
    name="Tony Stark",
    email="tonystark3000@gmail.com",
    age=65,
    weight=81.93,
    is_married=True,
    allergies=['Penicillin', 'Peanuts'],
    contact_details={
        "phone_number": "9123456780",
        "address": "Lane-8 Arvind Nagar Colony Shaikpet, Hyderabad (Telangana)"
    },
    linked_url="http://linkedin.com/123"
)

insert_patient_data(patient1)

patient2 = Patient(
    name="Jane Foster",
    email="janefoster1999@zohomail.com",
    age=28,
    weight=61.34,
    contact_details={
        "phone_number": "9123456780",
        "address": "Lane-2 Deluxe Colony Tolichowki, Hyderabad (Telangana)"
    }
)

insert_patient_data(patient2)

