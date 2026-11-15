from pydantic import BaseModel, Field, EmailStr
from typing import Annotated

class Address(BaseModel):
    city: str
    state: str
    pincode: int
    country: str

class Patient(BaseModel):
    name : Annotated[
        str,
        Field(
            max_length=50,
            description="Name of the patient must be in between 50 chars",
            examples=[""]
        )
    ]

    email: Annotated[EmailStr, Field(examples=['example@gmail.com'])]

    age: int = Field(gt=0, lt=120, strict=True)

    gender: str

    height: Annotated[float, Field(gt=0, strict=True)]

    weight: Annotated[float, Field(gt=0, strict=True)]

    address : Address


def insert_patient(patient : Patient):
    print(f"Patient Name: {patient.name}")
    print(f"Email: {patient.email}")
    print(f"Age: {patient.age}")
    print(f"Gender: {patient.gender}")
    print(f"Height: {patient.height}m")
    print(f"Weight: {patient.weight}kg")
    print(f"Address:\n\tCity: {patient.address.city}")
    print(f"\tState: {patient.address.state}")
    print(f"\tPin code: {patient.address.pincode}")
    print(f"\tCountry: {patient.address.country}")

address = Address(
    city="Hyderabad",
    state="Telangana",
    pincode=500008,
    country="India"
)

patient = Patient(
    name="Virat Kohli",
    email="Viratkohli2025@gmail.com",
    age=41,
    gender="MALE",
    height=1.81,
    weight=85.90,
    address=address
)

insert_patient(patient)


