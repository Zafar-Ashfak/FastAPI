from pydantic import BaseModel
from typing import List, Dict, Optional

class Patient(BaseModel):
    name : str # required
    email : str # required
    city : str # required
    age : int # required
    gender : str # required
    is_married : Optional[bool] = False # optional
    height : float | int # required
    weight : float | int # required
    allergies : Optional[List[str]] = None # optional
    contact : Dict[str, str] # required

def insert_patient(patient : Patient):
    print(f"Patient Name: {patient.name}")
    print(f"Email: {patient.email}")
    print(f"City: {patient.city}")
    print(f"Age: {patient.age}")
    print(f"Gender: {patient.gender}")
    print(f"Is Married: {patient.is_married}")
    print(f"Height: {patient.height}m")
    print(f"Weight: {patient.weight} kg")
    print(f"Allergies: {patient.allergies}")
    print(f"Contact Details: {patient.contact}")


patient1 = Patient(
    name="Sadie Sink",
    email="Sadiesink2002@gmail.com",
    city="New York",
    age=24,
    gender="FEMALE",
    height=1.2,
    weight=46.7,
    allergies=["Smoke", "Dust"],
    contact={
        "phone": "9123456789",
        "address": "Arvind Nagar Colony, Tolichowki, Hyderabad"
    }

)

patient2 = Patient(
    name="Peter Parker",
    email="Peterparker2001@gmail.com",
    city="New York",
    age=26,
    gender="MALE",
    is_married=True,
    height=1.8,
    weight=68.5,
    contact={
        "phone": "80b87654321",
        "address": "Rajiv Chowk, New Delhi, India"
    }
)

print("Patient - 1 records")
insert_patient(patient1)

print("\n\nPatient - 2 records")
insert_patient(patient2)

