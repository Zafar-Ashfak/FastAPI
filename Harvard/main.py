from typing import Annotated

from fastapi import FastAPI, HTTPException
import json

from fastapi.params import Path, Query

app = FastAPI()


# ********* HELPER METHOD ************
def load_data():
    with open("Harvard/students.json", "r") as file:
        return json.load(file)


# Create routes for home, about, services and contact
@app.get("/")
def home():
    return "This is HOME PAGE"


@app.get("/about")
def about():
    return "This is ABOUT PAGE"


@app.get("/services")
def services():
    return "This is SERVICES PAGE"


@app.get("/contact")
def contact():
    return "This is CONTACT PAGE"


# Create a route to fetch all students records
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


# Create a route to see a particular student record using Path parameter
@app.get("/students/{student_id}")
def get_student(
    student_id: Annotated[
        str,
        Path(
            ...,
            description="Enter ID of the student",
            examples=["s001"]
        )
    ]
):
    data = load_data()

    student = data.get(student_id)

    if student is None:
        raise HTTPException(
            status_code=404,
            detail=f"Student with ID '{student_id}' not found"
        )

    return {"id": student_id, **student}

# Create a route to filter students based on their course
@app.get("/filter")
def filter_students(
        course: Annotated[
            str,
            Query(...,
                  description="Enter course you want to check for student",
                  examples=["Python"]
                  )
        ]
):
    try:
        data = load_data()

        filtered_info = {}

        for student_id, info in data.items():
            if info["course"].lower() == course.lower():
                filtered_info[student_id] = info
        return filtered_info

    except FileNotFoundError:
        raise HTTPException(
            status_code=500,
            detail="Students data not found"
        )

# Create a route to sort student based on name, age, marks in asc or desc
@app.get("/sort")
def sort_students(sort_by, order):

    sort_fields = ["name", "roll", "age", "marks"]
    sort_order = ["asc", "desc"]

    if sort_order not in sort_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid field, choose from {sort_fields}"
        )

    data = load_data()

# Create a route to paginate student records
