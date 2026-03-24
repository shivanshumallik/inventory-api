# app/main.py

from fastapi import FastAPI
from app.core.database import engine
from app.models import item as item_model
from app.models import warehouse as warehouse_model
from app.models import inventory as inventory_model
from app.routers import items, warehouses, inventory

# Create all database tables on startup
# Order matters — Item and Warehouse must exist before Inventory
# because Inventory has foreign keys pointing to them
item_model.Base.metadata.create_all(bind=engine)
warehouse_model.Base.metadata.create_all(bind=engine)
inventory_model.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Inventory & Asset Management API",
    description="A backend API for tracking inventory items and assets across warehouses.",
    version="0.2.0",
)

# Register all routers with their URL prefixes and Swagger tags
app.include_router(items.router, prefix="/items", tags=["Items"])
app.include_router(warehouses.router, prefix="/warehouses", tags=["Warehouses"])
app.include_router(inventory.router, prefix="/inventory", tags=["Inventory"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the Inventory & Asset Management API v0.2.0"}