from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to Library Management System API"}

@app.get("/hello/{name}")
def greet(name: str):
    return {"message": f"Hello, {name}! Welcome to FastAPI."}
