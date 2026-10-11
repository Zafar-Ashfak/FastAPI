from pydantic import BaseModel, Field, EmailStr, HttpUrl, field_validator
from typing import List, Dict, Annotated, Optional

class Patient(BaseModel):
    name : Annotated[
        str,
        Field(
            max_length=50,
            title="Name of the patient",
            description="Give the full name of the patient",
            examples=["Ankit Kumar", "John Carter", "Sahil Khan"]
        )
    ]

    email : EmailStr

    age : int = Field(gt=0, lt=120)

    weight: float= Field(gt=0, lt=120, strict=True)

    height: float  # required

    bmi: float  # required

    is_married: Annotated[bool, Field(default=False, description="Is the patient married")] # Default

    allergies: Optional[List[str]] = None  # Optional List

    contact_details: Dict[str, str]

    linkedin_url : HttpUrl


    # Email field validation
    @field_validator('email')
    @classmethod
    def email_validation(cls, value : str):
        valid_domains = ["sbi.com", "hdfc.com"]
        domain_name = value.split("@")[-1]

        if domain_name not in valid_domains:
            raise ValueError("Invalid email")

        return value

    # name field validation in uppercase
    @field_validator('name')
    @classmethod
    def uppercase_name(cls, value : str):
        return value.upper()


def insert_patient_data(patient : Patient):
    print(f"Patient Name: {patient.name}")
    print(f"Email: {patient.email}")
    print(f"Age: {patient.age}")
    print(f"Weight: {patient.weight}kg")
    print(f"Height: {patient.height}cm")
    print(f"BMI: {patient.bmi}")
    print(f"Is_Married: {patient.is_married}")
    print(f"Allergies: {patient.allergies}")
    print(f"Contact Details: {patient.contact_details}")
    print(f"LinkedIn URL: {patient.linkedin_url}")
    print("\n")


patient1 = Patient(
    name="Tony Stark",
    email="tonystark3000@sbi.com",
    age=65,
    weight=81.32,
    height=179,
    bmi=26.86,
    is_married=True,
    contact_details={
        "phone number": "9123456780",
        "address": "Avengers tower, New york city, (America)"
    },
    linkedin_url="https://linkedin.com/tony-stark-3000"

)

insert_patient_data(patient1)


patient2 = Patient(
    name="Jane Foster",
    # email="Janefoster1999@gmail.com", # Raise an error, because domain_name is not in domain_names
    email="Janefoster1999@hdfc.com", # Code will work, because domain_name is in domain_names
    age=65,
    weight=81.32,
    height=179,
    bmi=26.86,
    is_married=True,
    contact_details={
        "phone number": "9123456780",
        "address": "Avengers tower, New york city, (America)"
    },
    linkedin_url="https://linkedin.com/tony-stark-3000"

)

insert_patient_data(patient2)

