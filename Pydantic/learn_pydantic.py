from pydantic import BaseModel, EmailStr, HttpUrl
from typing import List, Dict, Optional


class Patient(BaseModel):
    name: str  # required
    email: EmailStr
    age: int  # required
    weight: float  # required
    height: int  # required
    bmi: float  # required
    is_married: bool = False  # Default
    allergies: Optional[List[str]] = None  # Optional List
    contact_details: Dict[str, str]
    linkedin_url : HttpUrl


def insert_patient_data(patient: Patient):
    print(f"Patient Name: {patient.name}")
    print(f"Email: {patient.email}")
    print(f"Age: {patient.age}")
    print(f"Weight: {patient.weight}kg")
    print(f"Height: {patient.height}cm")
    print(f"BMI: {patient.bmi}")
    print(f"Is_Married : {patient.is_married}")
    print(f"Allergies: {patient.allergies}")
    print(f"Contact Details: {patient.contact_details}")
    print(f"LinkedIn URL: {patient.linkedin_url}")
    print("Record inserted successfully\n")


patient1 = Patient(
    name="Sifali Khan",
    email="Sifalikhan1996@gmail.com",
    age=30,
    weight=67.46,
    height=159,
    bmi=29.71,
    is_married=True,
    allergies=["Dust", "Smoke"],
    contact_details={
        "phone": "9012345678",
        "address": "Lane-8 Arvind Nagar Colony, Shaikpet, Hyderabad (Telangana)"
    },
    linkedin_url="https://linkedin.com/Sifali-Khan"
)

insert_patient_data(patient1)

patient2 = Patient(
    name="Ikra Shaikh",
    email="Ikrashaikhhyd2003@gmail.com",
    age=23,
    weight=47.46,
    height=146,
    bmi=18.34,
    contact_details={
        "phone": "9345678123",
        "address": "Lane-3 Rahul Colony, Tolichowki, Hyderabad (Telangana)"
    },
    linkedin_url="https://linkedin.com/Ikra-Shaikh_03"
)

insert_patient_data(patient2)
