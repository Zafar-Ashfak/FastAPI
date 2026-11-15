from pydantic import BaseModel, Field, EmailStr, AnyUrl
from typing import Optional, List, Dict, Annotated

class Patient(BaseModel):
    name : Annotated[
        str,
        Field(
            max_length=50,
            description="Name of the patient must be between 50 chars",
            examples=["Travis Head", "Aditi Chauhan"]
        )
    ]

    email : Annotated[EmailStr, Field(examples=['example@gmail.com'])]

    linkedin_url : AnyUrl

    city : str

    age : int = Field(gt=0, lt=120, strict=True)

    gender : str

    is_married : Annotated[bool, Field(default=False, description="Is the patient married")]

    height : Annotated[float, Field(gt=0, strict=True)]

    weight : Annotated[float, Field(gt=0, strict=True)]

    allergies : Optional[List[str]] = None

    contact : Dict[str, str]

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
    email="Sadiesink2002@gmail.com",
    linkedin_url="http://linkedin.com/Sadie-Sink",
    city="New York",
    age=23,
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

#
# patient2 = Patient(
#     name="Peter Parker",
#
#     email="Peterparker2001@zohomail.com",
#
#     linkedin_url="https://linkedin.com/Peter-Parker05",
#
#     city="New York",
#
#     age="26", # raise an error because data type is strictly check
#     gender="MALE",
#
#     is_married=True,
#
#     height="1.8", # raise an error because data type is strictly check
#
#     weight="68.4", # raise an error because data type is strictly check
#
#     contact={
#         "phone": "80b87654321",
#         "address": "Rajiv Chowk, New Delhi, India"
#     }
# )
#
# print("\n\nPatient - 2 records")
# insert_patient(patient2)
