from pydantic import BaseModel, Field, EmailStr, AnyUrl, computed_field
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):
    name : Annotated[
        str,
        Field(
            max_length=50,
            description="Name of the patient must be in between 50 chars",
            examples=["John Doe", "Imran Tahir"]
        )
    ]

    email : EmailStr

    linkedin : AnyUrl

    city : Annotated[
        str,
        Field(
            description="Name of the city from patient belongs to",
            examples=["New Delhi", "Hyderabad"]
        )
    ]

    age : Annotated[int, Field(ge=0, le=120, strict=True)]

    is_married: Annotated[bool, Field(default=False, description="Is the patient married")]

    height: Annotated[float, Field(gt=0, strict=True)]

    weight: Annotated[float, Field(gt=0, strict=True)]

    allergies: Optional[List[str]] = None

    contact: Dict[str, str]


    @computed_field
    @property
    def bmi(self) -> float | int:
        return round((self.weight / self.height ** 2), 2)

def insert_patient(patient : Patient):
    print(f"Patient Name: {patient.name}")
    print(f"Email: {patient.email}")
    print(f"LinkedIn: {patient.linkedin}")
    print(f"City: {patient.city}")
    print(f"Age: {patient.age}")
    print(f"Is Married: {patient.is_married}")
    print(f"Height: {patient.height}m")
    print(f"Weight: {patient.weight} kg")
    print(f"Allergies: {patient.allergies}")
    print(f"Contact: {patient.contact}")
    print(f"BMI: {patient.bmi}")

patient1 = Patient(
    name="Sadie Sink",
    email="Sadiesink2002@gmail.com",
    linkedin="https://linkedin.com/Sadie-Sink",
    city="New York City",
    age=24,
    height=1.60,
    weight=47.40,
    contact={
        "phone": "9123456789",
        "address": "New York City, America"
    }
)

insert_patient(patient1)
