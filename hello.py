from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello():
    return {
        "message" : "Intellica"
    }

@app.get("/about")
def about():
    return {
        "message": "Intellica is a multi-agent research system designed to provide accurate and research-based answers to user queries."
    }