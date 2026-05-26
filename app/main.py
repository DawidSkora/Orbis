from fastapi import FastAPI

app = FastAPI(title="Orbis")

@app.get("/")
def root():
    return {"status": "Orbis is running"}

@app.get("/data")
def get_data():
    return {
        "message": "Hello from Orbis",
        "items": ["alpha", "beta", "gamma"]
    }