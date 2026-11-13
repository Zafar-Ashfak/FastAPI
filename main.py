from fastapi import FastAPI
app = FastAPI()
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