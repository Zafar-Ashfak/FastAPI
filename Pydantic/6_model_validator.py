from pydantic import BaseModel, Field, EmailStr, AnyUrl, model_validator
from typing import Optional, List, Dict, Annotated

class Patient(BaseModel):
    name : Annotated[
        str,
        Field(
            max_length=50,
            description="Name of the patient must be between 50 chars",
            examples=["Travis Head", "Rohit Sharma"]
        )
    ]

    email : EmailStr

    linkedin_url: AnyUrl

    city: str

    age: int = Field(gt=0, lt=120, strict=True)

    gender: str

    is_married: Annotated[bool, Field(default=False, description="Is the patient married")]

    height: Annotated[float, Field(gt=0, strict=True)]

    weight: Annotated[float, Field(gt=0, strict=True)]

    allergies: Optional[List[str]] = None

    contact: Dict[str, str]

    # Create a validator to check patient older than 60 has an emergency contact number
    @model_validator(mode="after")
    @classmethod
    def validate_emergency_contact(cls, model):
        if model.age > 60 and "emergency" not in model.contact:
            raise ValueError("Patient older than 60 must have emergency contact number")

        return model


def insert_patient(patient : Patient):
    print(f"Patient Name: {patient.name}")
    print(f"Email: {patient.email}")
    print(f"LinkedIn: {patient.linkedin_url}")
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
    email="Sadiesink2002@sbi.com",
    linkedin_url="https://linkedin.com/Sadie-Sink",
    city="New York City",
    age=24,
    gender="FEMALE",
    height=1.2,
    weight=46.7,
    allergies=["Smoke", "Dust"],
    contact={
        "phone": "9123456789",
        "address": "New York City, America"
    }
)

insert_patient(patient1)

patient1 = Patient(
    name="Tony Stark",
    email="Tonystark3000@ironman.com",
    linkedin_url="https://linkedin.com/Tony-Stark",
    city="New York City",
    age=65,                   # Age > 60 must have emergency number in contact
    gender="MALE",
    height=1.8,
    weight=79.3,
    contact={
        "phone": "9123456789",
        "address": "New York City, America"
    }
)

insert_patient(patient1)
