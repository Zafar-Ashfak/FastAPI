# Create a Pydantic model for Student

from pydantic import BaseModel, EmailStr, Field, field_validator, computed_field
from typing import Annotated, List
import json

# Annotate each field and validate data type
class Student(BaseModel):
    id : Annotated[str, Field(description="Unique ID of the student", examples=["s001"])]
    name : Annotated[str, Field(max_length=50, description="Name of the student", examples=["Bruce Wayne"])]
    email : Annotated[EmailStr, Field(examples=["example@gmail.com"])]
    roll : Annotated[int, Field(ge=1, description="Roll number of the student", examples=[101])]
    age : Annotated[int, Field(ge=5, lt=100, examples=["101"])]
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


def insert_student(student : Student):
    print(f"Student ID: {student.id}")
    print(f"Name: {student.name}")
    print(f"Email: {student.email}")
    print(f"Roll: {student.roll}")
    print(f"Age: {student.age}")
    print(f"Course: {student.course}")
    print(f"Marks: {student.marks}")
    print(f"Skills: {student.skills}")
    print(f"Grade: {student.grade}")

student_dict = {
    "id" : "s001",
    "name" : "Sidra Fatima",
    "email" : "Sidrafatima2023@gmail.com",
    "roll" : 101,
    "age": 7,
    "course" : "Agentic AI",
    "marks" : 97.46,
    "skills": ["Python", "Numpy", "Pandas", "ML", "DL", "GenAI"]
}

student1 = Student(**student_dict)

insert_student(student1)

# Load student records and validate using Pydantic model
def load_data():
    with open("students.json", "r") as file:
        return json.load(file)


data = load_data()

print("\n\nStudents.json file data\n")

for student_id, info in data.items():
    student = Student(id = student_id, **info)
    print(student.model_dump())

