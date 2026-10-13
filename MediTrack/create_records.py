import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, Field, computed_field
from typing import List, Annotated, Literal, Optional
import json
app = FastAPI()

class Patient(BaseModel):
    id : Annotated[str, Field(..., title="ID of the patient", examples=["p001"])]

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

    allergies: Optional[List[str]] = None

    # calculating patient's BMI
    @computed_field(return_type=float)
    @property
    def bmi(self):
        return round(self.weight / (self.height ** 2), 2)

    # calculating patients bmi category
    @computed_field(return_type=str)
    @property
    def bmi_category(self):
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 25:
            return "Healthy weight"
        elif self.bmi < 30:
            return "Overweight"
        else:
            return "Obese"


def load_data():
    with open("MediTrack/patients.json", "r") as file:
        data = json.load(file)

    return data

def save_data(data):
    with open("MediTrack/patients.json", 'w') as file:
        json.dump(data, file)


@app.post("/create", status_code=201)
def create_patient(patient: Patient):
    # Load data
    data = load_data()

    # Check if the patient already exists
    if patient.id in data:
        raise HTTPException(
            status_code=400,
            detail=f"Patient with ID {patient.id} already exists"
        )

    data[patient.id] = patient.model_dump(exclude='id')

    # save in the json
    save_data(data)
    return JSONResponse(
        status_code=201,
        content="Patient record created successfully"
    )

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8001)