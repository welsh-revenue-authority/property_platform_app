from fastapi import FastAPI

app = FastAPI()

@app.get("/api")
def read_api_root():
    return {"Hello": "World"}