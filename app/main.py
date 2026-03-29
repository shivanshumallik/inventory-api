# app/main.py

from fastapi import FastAPI
from app.core.config import settings
from app.core.exceptions import register_exception_handlers
from app.routers import items, warehouses, inventory, auth

app = FastAPI(
    title=settings.APP_NAME,
    description="""
## Inventory & Asset Management API

A production-ready backend API for managing inventory across multiple warehouses.

### Features
* 🔐 **JWT Authentication** with role-based access (Admin/Staff)
* 📦 **Item Management** with filtering and search
* 🏭 **Multi-Warehouse** stock management
* 📊 **Low Stock Alerts** with configurable thresholds
* 🗄️ **Database Migrations** with Alembic

### How to Use
1. Register at `/auth/register`
2. Login at `/auth/login` to get your JWT token
3. Click **Authorize** 🔒 and enter: `Bearer <your_token>`
4. All protected endpoints will work automatically
    """,
    version=settings.APP_VERSION,
    contact={
        "name": "Inventory API Support",
        "email": "support@inventory-api.com"
    },
    license_info={
        "name": "MIT License"
    }
)

register_exception_handlers(app)

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(items.router, prefix="/items", tags=["Items"])
app.include_router(warehouses.router, prefix="/warehouses", tags=["Warehouses"])
app.include_router(inventory.router, prefix="/inventory", tags=["Inventory"])


@app.get("/", tags=["Health"])
def read_root():
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "healthy"}