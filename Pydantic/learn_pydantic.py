from pydantic import BaseModel
from typing import List, Dict

class Patient(BaseModel):
    name : str
    age : int
    weight : float
    height : int
    bmi : float
    is_married : bool
    allergies : List[str]
    contact_details : Dict[str, str]

def insert_patient_data(patient : Patient):
    print(f"Patient Name: {patient.name}")
    print(f"Age: {patient.age}")
    print(f"Weight: {patient.weight}kg")
    print(f"Height: {patient.height}cm")
    print(f"BMI: {patient.bmi}")
    print(f"Is_Married : {patient.is_married}")
    print(f"Allergies: {patient.allergies}")
    print(f"Contact Details: {patient.contact_details}")

patient1 = Patient(
    name="Aditi Singh",
    age=30,
    weight=67.46,
    height=159,
    bmi=29.71,
    is_married=True,
    allergies=["Dust", "Smoke"],
    contact_details={
        "email": "aditisingh1996@gmail.com",
        "phone": "9012345678",
        "address": "Aashiyana Colony, Baghmali, Hajipur (Bihar)"
    }
)



insert_patient_data(patient1)