from fastapi import FastAPI, HTTPException
import json

from fastapi.params import Path

app = FastAPI()

def load_data():
    with open("students.json", "r") as file:
        return json.load(file)
@app.get("/")
def home():
    return "Welcome to My Website! Hello! I'm Zafar Ashfaq. Welcome to my personal website."

@app.get("/about")
def about():
    return "I'm Zafar Ashfaq, a technology enthusiast passionate about building modern applications and exploring innovative technologies."

@app.get("/services")
def services():
    return "My Services \nI offer services focused on building reliable and efficient digital solutions."

@app.get("/contact")
def contact():
    return "# Get in Touch. Have a question, project idea, or collaboration opportunity?"

@app.get("/students")
def get_students():
    try:
        data = load_data()

        return data
    except FileNotFoundError:
        raise HTTPException(
            status_code=500,
            detail="Students data not found"
        )


# Path Parameter
@app.get("/students/{student_id}")
def get_student(
    student_id: str = Path(
        ...,
        description="ID of the student",
        examples=["s001"]
    )
):
    data = load_data()

    if student_id not in data:
        raise HTTPException(
            status_code=404,
            detail=f"Student with ID {student_id} not found"
        )

    return data[student_id]