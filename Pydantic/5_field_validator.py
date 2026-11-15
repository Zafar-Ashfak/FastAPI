from pydantic import BaseModel, Field, EmailStr, AnyUrl, field_validator
from typing import Optional, List, Dict, Annotated

class Patient(BaseModel):
    name: Annotated[
        str,
        Field(
            max_length=50,
            description="Name of the patient must be between 50 chars",
            examples=["Travis Head", "Aditi Chauhan"]
        )
    ]

    email: Annotated[EmailStr, Field(examples=['example@gmail.com'])]

    linkedin_url: AnyUrl

    city: str

    age: int = Field(gt=0, lt=120, strict=True)

    gender: str

    is_married: Annotated[bool, Field(default=False, description="Is the patient married")]

    height: Annotated[float, Field(gt=0, strict=True)]

    weight: Annotated[float, Field(gt=0, strict=True)]

    allergies: Optional[List[str]] = None

    contact: Dict[str, str]

    # Validate Email based on employee email domain name such as :- sbi.com, hdfc.com, axis.com
    @field_validator('email')
    @classmethod
    def email_validation(cls, value):
        valid_domains = ["sbi.com", "hdfc.com", "axis.com"]

        domain_name = value.split('@')[-1]
        if domain_name not in valid_domains:
            raise ValueError("Domain name doesn't match")

        return value

    # Validate Name of the patent in uppercase
    @field_validator('name')
    @classmethod
    def to_uppercase(cls, value):
        return value.upper()

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


# patient2 = Patient(
#     name="Peter Parker",
#
#     # email="Peterparker2001@zohomail.com",   # Value error :- domain name doesn't match
#
#     linkedin_url="https://linkedin.com/Peter-Parker05",
#
#     city="New York",
#
#     age=26,
#     gender="MALE",
#
#     is_married=True,
#
#     height=1.8,
#
#     weight=68.4,
#
#     contact={
#         "phone": "80b87654321",
#         "address": "Rajiv Chowk, New Delhi, India"
#     }
# )
#
# print("\n\nPatient - 2 records")
# insert_patient(patient2)