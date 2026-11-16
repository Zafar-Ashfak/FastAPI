from fastapi import FastAPI, HTTPException
import json

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
            detail="Student data not found"
        )

# Create a route to see a particular student record using Path parameter
# Create a route to filter students based on their course
# Create a route to sort student based on name, age, marks in asc or desc
# Create a route to paginate student records
