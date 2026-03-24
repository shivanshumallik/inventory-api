# app/routers/warehouses.py

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.warehouse import WarehouseCreate, WarehouseUpdate, WarehouseResponse
from app.services import warehouse_service

router = APIRouter()


@router.get("/", response_model=List[WarehouseResponse])
def get_warehouses(db: Session = Depends(get_db)):
    """Get all active warehouses"""
    return warehouse_service.get_all_warehouses(db)


@router.get("/{warehouse_id}", response_model=WarehouseResponse)
def get_warehouse(warehouse_id: int, db: Session = Depends(get_db)):
    """Get a specific warehouse by ID"""
    return warehouse_service.get_warehouse_by_id(db, warehouse_id)


@router.post("/", response_model=WarehouseResponse, status_code=status.HTTP_201_CREATED)
def create_warehouse(warehouse: WarehouseCreate, db: Session = Depends(get_db)):
    """Create a new warehouse"""
    return warehouse_service.create_warehouse(db, warehouse)


@router.put("/{warehouse_id}", response_model=WarehouseResponse)
def update_warehouse(
    warehouse_id: int,
    warehouse: WarehouseUpdate,
    db: Session = Depends(get_db)
):
    """Update warehouse details"""
    return warehouse_service.update_warehouse(db, warehouse_id, warehouse)