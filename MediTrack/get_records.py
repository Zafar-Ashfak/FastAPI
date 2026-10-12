from fastapi import FastAPI, HTTPException, Path, Query
import json

app = FastAPI()


def load_data():
    with open("MediTrack/patients.json", "r") as file:
        data = json.load(file)

    return data


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
    example="p001"
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
