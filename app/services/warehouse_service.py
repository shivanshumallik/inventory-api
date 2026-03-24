# app/services/warehouse_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.warehouse import Warehouse
from app.schemas.warehouse import WarehouseCreate, WarehouseUpdate


def get_all_warehouses(db: Session) -> list[Warehouse]:
    """Get all active warehouses"""
    return db.query(Warehouse).filter(Warehouse.is_active == True).all()


def get_warehouse_by_id(db: Session, warehouse_id: int) -> Warehouse:
    """Get a single warehouse or raise 404"""
    warehouse = db.query(Warehouse).filter(
        Warehouse.id == warehouse_id,
        Warehouse.is_active == True
    ).first()

    if not warehouse:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Warehouse with id {warehouse_id} not found"
        )
    return warehouse


def create_warehouse(db: Session, warehouse_data: WarehouseCreate) -> Warehouse:
    """Create a new warehouse"""

    # Check if a warehouse with the same name already exists
    existing = db.query(Warehouse).filter(
        Warehouse.name == warehouse_data.name
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Warehouse with name '{warehouse_data.name}' already exists"
        )

    db_warehouse = Warehouse(**warehouse_data.model_dump())
    db.add(db_warehouse)
    db.commit()
    db.refresh(db_warehouse)
    return db_warehouse


def update_warehouse(
    db: Session,
    warehouse_id: int,
    warehouse_data: WarehouseUpdate
) -> Warehouse:
    """Update warehouse details"""
    db_warehouse = get_warehouse_by_id(db, warehouse_id)

    update_data = warehouse_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_warehouse, field, value)

    db.commit()
    db.refresh(db_warehouse)
    return db_warehouse