from fastapi import FastAPI
import json
from pathlib import Path
app = FastAPI()

def load_data():
    file_path = Path(__file__).parent / "patients.json"
    with open(file_path, "r") as file:
        data = json.load(file)

    return data

# Create a home page request
@app.get("/")
def home():
    return {
        "message": "Welcome to MediTrack API",
        "description": "A secure and scalable REST API for managing patient records and healthcare information."
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