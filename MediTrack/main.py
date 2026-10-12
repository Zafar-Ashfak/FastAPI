from fastapi import FastAPI, HTTPException, Path, Query
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

@app.get("/")
def home():
    return "Welcome to MediTrack"

@app.get("/about")
def about():
    return {
        "message": "MediTrack Patient Management System",
        "description": "A backend service designed to create, retrieve, update, and manage patient records through RESTful APIs."
    }

@app.get("/patients")
def get_patients():
    try:
        data = load_data()
        return data

    except FileNotFoundError:
        raise HTTPException(
            status_code=500,
            detail="Patient data file not found"
        )

    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500,
            detail="Patient data file contains invalid JSON"
        )

@app.get("/patients/{patient_id}")
def get_patient(patient_id: str = Path(
    ...,
    title="MediTrack",
    description="ID of the patient in the DB",
    examples=["p001"]
)):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(
            status_code=404,
            detail=f"Patient with ID {patient_id} not found"
        )

    return data[patient_id]

@app.get("/sort")
def sort_patients(sort_by: str = Query(
    ...,
    description="Sort by height, weight or BMI",
), order: str = Query(
    "asc",
    description="Sort order: asc or desc"
)):
    valid_fields = ["height", "weight", "bmi"]
    valid_orders = ["asc", "desc"]

    if sort_by not in valid_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid fields, choose from {valid_fields}"
        )

    if order not in valid_orders:
        raise HTTPException(
            status_code=400,
            detail="Invalid field, choose asc or desc"
        )

    data = load_data()

    sorted_data = sorted(data.values(), key=lambda patient: patient.get(sort_by, 0), reverse=(order == "desc"))

    return sorted_data

@app.post("/create", status_code=201)
def create_patient(patient: Patient):
    # Load data
    data = load_data()

    # Check if the patient already exists
    if patient.id in data:
        raise HTTPException(
            status_code=400,
            detail=f"Patient with ID {patient.id} already exits"
        )

    data[patient.id] = patient.model_dump(exclude=['id'])

    # save in the json
    save_data(data)
    return JSONResponse(
        status_code=201,
        content="Patient record created successfully"
    )
