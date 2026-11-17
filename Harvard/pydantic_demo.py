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

def insert_student(s : Student):
    print(f"Student ID: {s.id}")
    print(f"Name: {s.name}")
    print(f"Email: {s.email}")
    print(f"Roll: {s.roll}")
    print(f"Age: {s.age}")
    print(f"Course: {s.course}")
    print(f"Marks: {s.marks}")
    print(f"Skills: {s.skills}")

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

