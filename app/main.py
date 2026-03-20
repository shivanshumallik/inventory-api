# app/main.py

from fastapi import FastAPI
from app.routers import items
from app.core.database import engine
from app.models import item as item_model

item_model.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Inventory & Asset Management API",
    description="A backend API for tracking inventory items and assets.",
    version="0.1.0",
)

app.include_router(items.router, prefix="/items", tags=["Items"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Inventory & Asset Management API"}