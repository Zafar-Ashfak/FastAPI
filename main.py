from fastapi import FastAPI
app = FastAPI()
@app.get("/")
def greet():
    return "Hi, I am Zafar Ashfaq."