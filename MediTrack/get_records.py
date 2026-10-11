from fastapi import FastAPI, Path, HTTPException, Query
import json
app = FastAPI()

def load_data():
    with open("MediTrack/patients.json", "r") as file:
        data = json.load(file)

    return data

# Create a home page request
@app.get("/")
def home():
    return {
        "message": "Welcome to MediTrack API"
    }

@app.get("/about")
def about():
    return {
        "message": "MediTrack Patient Management System",
        "description": "A backend service designed to create, retrieve, update, and manage patient records through RESTful APIs."
    }


@app.get("/patients")
def get_patients():
    data = load_data()
    return data

@app.get("/patients/{patient_id}")
def get_patient(patient_id : str = Path(
    ..., title="MediTrack", description="ID of the patient in the DB", example="p001"
)):
    data = load_data()
    if patient_id in data:
        return data[patient_id]

    raise HTTPException(
        status_code=404,
        detail=f"Patient with ID {patient_id} not found"
    )

@app.get("/sort")
def sort_patients(
        sort_by : str = Query(
            ..., description="Sort by height, weight or BMI",
            examples=["height"]
        ),
        order : str = Query(
            "asc",
            description="Sort order: asc or desc",
            examples=["asc"]
        )
):
    valid_fields = ["height", "weight", "bmi"]
    valid_orders = ["asc", "desc"]

    if sort_by not in valid_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid field. Choose from {valid_fields}"
        )

    if order not in valid_orders:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid field. Choose 'asc' or 'desc'"
        )

    data = load_data()

    sorted_data = sorted(data.values(), key= lambda patient : patient.get(sort_by, 0), reverse=(order=='desc'))

    return sorted_data
