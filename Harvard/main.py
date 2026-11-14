from fastapi import FastAPI, HTTPException
import json

from fastapi.params import Path, Query
from typing import Annotated

app = FastAPI()


def load_data():
    with open("Harvard/students.json", "r") as file:
        data = json.load(file)

    return data


@app.get("/")
def home():
    return ("Welcome to Harvard University, where knowledge meets innovation and excellence inspires"
            "generations.")


@app.get("/about")
def about():
    return ("Harvard University is committed to academic excellence, innovation, and research. We empower"
            "students with knowledge, skills, and opportunities to become future leaders and make a"
            "positive impact on society."
            )


@app.get("/services")
def services():
    return ("At Harvard University, we provide a wide range of academic and student support services"
            "designed to enhance the learning experience. From academic advising and research"
            "opportunities to career development and library resources, we ensure students have the tools"
            "they need to succeed.")


@app.get("/contact")
def contact():
    return ("We would love to hear from you. Whether you have questions about admissions, academic"
            "programs, campus facilities, or student services, our team is here to help. Reach out to us"
            "for information and assistance. We look forward to connecting with you and helping you take"
            "the next step in your academic journey.")


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
        student_id: Annotated[str, Path(
            ...,
            description="ID of the student",
            examples=["s001"]
        )]
):
    data = load_data()

    if student_id not in data:
        raise HTTPException(
            status_code=404,
            detail=f"Student with ID {student_id} not found"
        )

    return data[student_id]


# Query Parameter

@app.get("/filter")
def filter_students(
    course: Annotated[str, Query(
        ...,
        description="Enter course to filter data",
        examples=["Generative AI"]
    )]
):
    data = load_data()

    filtered_info = {}

    for student_id, info in data.items():
        if info["course"].lower() == course.lower():
            filtered_info[student_id] = info

    if not filtered_info:
        raise HTTPException(
            status_code=404,
            detail=f"No students found for course: {course}"
        )

    return filtered_info

@app.get("/sort")
def sort_students(
        sort_by : Annotated[str, Query(
            ..., description="Sort by age or marks",
            examples=["marks"]
        )],

        order: Annotated[str, Query(
            description="Sort order: asc or desc"
        )] = "asc"
):

    sort_fields = ["name", "age", "marks"]
    sort_order = ["asc", "desc"]

    if sort_by not in sort_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid fields, choose from {sort_fields}"
        )

    if order not in sort_order:
        raise HTTPException(
            status_code=400,
            detail="Invalid field, choose asc or desc"
        )


    data = load_data()

    sorted_data = sorted(data.values(), key=lambda student : student.get(sort_by, 0), reverse=order== "desc")
    return sorted_data
