from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field
from typing import List, Annotated, Literal, Optional

app = FastAPI()


class Patient(BaseModel):
    name: Annotated[
        str,
        Field(...,
              max_length=50,
              title="Name of the patient",
              description="Give the full name of the patient",
              examples=["Vikram Reddy"]
        )
    ]

    email: EmailStr
    city: Annotated[str, Field(
        description="Name of the city the patient is from"
    )]

    age: Annotated[int, Field(
        gt=0,
        lt=120,
    )]

    gender: Annotated[Literal["MALE", "FEMALE", "OTHER"], Field(
        description="Patient's gender must be in uppercase"
    )]

    height: Annotated[float, Field(gt=0)]

    weight: Annotated[float, Field(gt=0)]

    allergies: Optional[List[str]]



