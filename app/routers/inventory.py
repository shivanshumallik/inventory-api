# app/routers/inventory.py

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.inventory import (
    InventoryCreate,
    InventoryResponse,
    StockAdjustment,
    StockSummaryResponse
)
from app.services import inventory_service

router = APIRouter()


@router.post("/", response_model=InventoryResponse, status_code=status.HTTP_201_CREATED)
def add_stock(inventory: InventoryCreate, db: Session = Depends(get_db)):
    """
    Add stock for an item in a warehouse.
    If stock entry already exists, quantity is added to existing.
    """
    return inventory_service.add_stock_to_warehouse(db, inventory)


@router.put("/reduce/{item_id}/{warehouse_id}", response_model=InventoryResponse)
def reduce_stock(
    item_id: int,
    warehouse_id: int,
    adjustment: StockAdjustment,
    db: Session = Depends(get_db)
):
    """Reduce stock for an item in a specific warehouse"""
    return inventory_service.reduce_stock(db, item_id, warehouse_id, adjustment)


@router.get("/item/{item_id}", response_model=List[StockSummaryResponse])
def get_stock_by_item(item_id: int, db: Session = Depends(get_db)):
    """Get stock levels for one item across all warehouses"""
    return inventory_service.get_stock_for_item(db, item_id)


@router.get("/warehouse/{warehouse_id}", response_model=List[StockSummaryResponse])
def get_stock_by_warehouse(warehouse_id: int, db: Session = Depends(get_db)):
    """Get all stock in a specific warehouse"""
    return inventory_service.get_stock_for_warehouse(db, warehouse_id)