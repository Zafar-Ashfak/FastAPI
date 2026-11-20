from typing import Annotated, List
from pydantic import BaseModel, Field, EmailStr, field_validator, computed_field

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json

from fastapi.params import Path, Query
from fastapi.responses import JSONResponse

app = FastAPI()

#CORS-> CROSS ORIGIN RESOURCE SHARING
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)



class Student(BaseModel):
    id : Annotated[str, Field(description="Unique ID of the student", examples=["S001"])]
    name : Annotated[str, Field(max_length=50, description="Name of the student")]
    email : Annotated[EmailStr, Field(examples=["example@gmail.com"])]
    roll : Annotated[int, Field(ge=1, description="Roll number of the student", examples=[101])]
    age : Annotated[int, Field(ge=5, lt=100, examples=["21"])]
    course : Annotated[str, Field(examples=["Generative AI"])]
    marks : Annotated[float | int, Field(ge=0, le=100, examples=[99.9])]
    skills : Annotated[List[str], Field(max_length=10)]

    # validate name field to check name contains only alphabet

    @field_validator("name")
    @classmethod
    def validate_name(cls, value : str):
        if not value.replace(" ", "").isalpha():
            raise ValueError("Name must contain alphabet only")

        return value.title()


    # compute marks field and create a new field grade

    @computed_field
    @property
    def grade(self) -> str:
        if self.marks >= 90:
            return "A+"
        elif self.marks >= 80:
            return "A"
        elif self.marks >= 70:
            return "AB"
        elif self.marks >= 60:
            return "B"
        elif self.marks >= 50:
            return "BC"
        elif self.marks >= 40:
            return "C"
        else:
            return "F"

class UpdateStudent(BaseModel):
    name: Annotated[str | None, Field(default= None, max_length=50, description="Name of the student")]
    email: Annotated[EmailStr | None, Field(default=None, examples=["example@gmail.com"])]
    roll: Annotated[int | None, Field(default=None, ge=1, description="Roll number of the student", examples=[101])]
    age: Annotated[int | None, Field(default=None, ge=5, lt=100, examples=["21"])]
    course: Annotated[str | None, Field(default=None, examples=["Generative AI"])]
    marks: Annotated[float | int | None, Field(default=None, ge=0, le=100, examples=[99.9])]
    skills: Annotated[List[str] | None, Field(default=None, max_length=10)]

# ********* HELPER METHOD ************
def load_data():
    with open("students.json", "r") as file:
        return json.load(file)

def save_data(data):
    with open("students.json", "w") as file:
        json.dump(data, file, indent=4)


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
                examples=["S001"]
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
def sort_students(
        sort_by: Annotated[
            str,
            Query(...,
                  description="Sort by name, roll, age or marks",
                  examples=["name : Bruce Wayne", "roll : 101", "age : 21", "marks : 98.6"]
                  )],

        order: Annotated[str, Query(description="Sort order: asc or desc")] = "asc"
):
    sort_fields = ["name", "roll", "age", "marks"]
    sort_order = ["asc", "desc"]

    if sort_by not in sort_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid field, choose from {sort_fields}"
        )

    if order not in sort_order:
        raise HTTPException(
            status_code=400,
            detail="Invalid field, choose asc or desc"
        )

    data = load_data()

    sorted_data = sorted(data.values(), key=lambda student: student.get(sort_by, 0), reverse=order == "desc")
    return sorted_data


# Create a route to paginate student records
@app.get("/paginate")
def pagination(
        page: Annotated[int, Query(ge=1)] = 1,
        limit: Annotated[int, Query(ge=1, le=100)] = 3
):

    data = load_data()

    student_list = []

    # Turing dictionary into alist
    for student_id, info in data.items():
        student_list.append({"id": student_id, **info})

    start = (page - 1) * limit
    end = start + limit

    page_student = student_list[start: end]
    total_students = len(student_list)

    return {
        "page": page,
        "limit": limit,
        "total students": total_students,
        "page_student": page_student
    }

@app.post("/create", status_code=201)
def create_student(student : Student):
    data = load_data()

    if student.id in data:
        raise HTTPException(
            status_code=409,
            detail=f"Student with ID {student.id} already exists"
        )

    data[student.id] = student.model_dump(exclude="id")

    save_data(data)

    return JSONResponse(
        status_code=201,
        content="Student record created successfully"
    )

@app.put("/update/{student_id}")
def update_student(
        student_id : Annotated[str, Path(..., description="Id of the student", examples=["S001"])]
        ,update_student : UpdateStudent
):

    data = load_data()

    if student_id not in data:
        raise HTTPException(
            status_code=404,
            detail=f"Student with ID {student_id} not found"
        )

    updated_student_info = update_student.model_dump(exclude_unset=True)

    exising_student_info = data[student_id]

    for key, value in updated_student_info.items():
        exising_student_info[key] = value

    student = Student(id=student_id, **exising_student_info)

    data[student_id] = student.model_dump(exclude="id")

    save_data(data)

    return JSONResponse(
        status_code=200,
        content="Student updated successfully"
    )

@app.delete("/delete/{student_id}")
def delete_student(student_id : Annotated[str, Path(..., description="ID of the student", examples=["S001"])]):
    data = load_data()

    if student_id not in data:
        raise HTTPException(
            status_code=404,
            detail=f"Student with ID {student_id} not found"
        )

    del data[student_id]

    save_data(data)

    return JSONResponse(
        status_code=200,
        content="Student deleted successfully"
    )





