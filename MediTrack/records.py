from fastapi import FastAPI, Path, HTTPException
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



