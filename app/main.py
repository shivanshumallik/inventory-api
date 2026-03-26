# app/main.py

from fastapi import FastAPI
from app.routers import items, warehouses, inventory
from app.core.exceptions import register_exception_handlers

app = FastAPI(
    title="Inventory & Asset Management API",
    description="A backend API for tracking inventory items and assets across warehouses.",
    version="0.3.0",
)


register_exception_handlers(app)

app.include_router(items.router, prefix="/items", tags=["Items"])
app.include_router(warehouses.router, prefix="/warehouses", tags=["Warehouses"])
app.include_router(inventory.router, prefix="/inventory", tags=["Inventory"])


@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Inventory & Asset Management API",
        "version": "0.3.0",
        "docs": "/docs"
    }