# main.py
from fastapi import FastAPI
from app.routers import flights_router

app = FastAPI(title="Sepehran Flights API", version="0.1.0")
app.include_router(flights_router)

@app.get("/")
def root():
    return {"status": "ok"}
