from pydantic import BaseModel, Field, EmailStr, AnyUrl
from typing import Optional, List, Dict

class Patient(BaseModel):
    name : str = Field(max_length=50) # required
    email : EmailStr # required
    linkedin_url : AnyUrl
    city : str # required
    age : int = Field(gt=0, lt=120) # required
    gender : str # required
    is_married : Optional[bool] = False # optional
    height : float | int = Field(gt=0) # required
    weight : float | int = Field(gt=0) # required
    allergies : Optional[List[str]] = None # optional
    contact : Dict[str, str] # required

def insert_patient(patient : Patient):
    print(f"Patient Name: {patient.name}")
    print(f"Email: {patient.email}")
    print(f"Email: {patient.linkedin_url}")
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
    linkedin_url="http://linkedin.com/Zafar-Ashfaq",
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

insert_patient(patient1)


patient2 = Patient(
    name="Peter Parker",
    email="Peterparker2001gmail.com", # raise an error
    linkedin_url="https://linkedin.com/Zafar-Ashfaq", # raise an error
    city="New York",
    age=26,
    gender="MALE",
    height=-1.2, # raise an error
    weight=-46.7, # raise an error
    contact={
        "phone": "9123456789",
        "address": "Arvind Nagar Colony, Tolichowki, Hyderabad"
    }
)

insert_patient(patient2)

