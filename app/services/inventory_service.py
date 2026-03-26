# app/services/inventory_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.inventory import Inventory
from app.models.item import Item
from app.models.warehouse import Warehouse
from app.schemas.inventory import (
    InventoryCreate,
    StockAdjustment,
    StockSummaryResponse,
    LowStockAlertResponse
)


def _verify_item_exists(db: Session, item_id: int) -> Item:
    item = db.query(Item).filter(
        Item.id == item_id,
        Item.is_active == True
    ).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found"
        )
    return item


def _verify_warehouse_exists(db: Session, warehouse_id: int) -> Warehouse:
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


def add_stock_to_warehouse(db: Session, inventory_data: InventoryCreate) -> Inventory:
    """Add stock for an item in a warehouse"""
    _verify_item_exists(db, inventory_data.item_id)
    _verify_warehouse_exists(db, inventory_data.warehouse_id)

    existing = db.query(Inventory).filter(
        Inventory.item_id == inventory_data.item_id,
        Inventory.warehouse_id == inventory_data.warehouse_id
    ).first()

    if existing:
        existing.quantity += inventory_data.quantity
        existing.threshold = inventory_data.threshold
        db.commit()
        db.refresh(existing)
        return existing
    else:
        new_entry = Inventory(**inventory_data.model_dump())
        db.add(new_entry)
        db.commit()
        db.refresh(new_entry)
        return new_entry


def reduce_stock(
    db: Session,
    item_id: int,
    warehouse_id: int,
    adjustment: StockAdjustment
) -> Inventory:
    """Reduce stock — cannot go below zero"""
    _verify_item_exists(db, item_id)
    _verify_warehouse_exists(db, warehouse_id)

    inventory_entry = db.query(Inventory).filter(
        Inventory.item_id == item_id,
        Inventory.warehouse_id == warehouse_id
    ).first()

    if not inventory_entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No stock entry found for this item in this warehouse"
        )

    if inventory_entry.quantity < adjustment.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Insufficient stock. Available: {inventory_entry.quantity}, "
                   f"Requested: {adjustment.quantity}"
        )

    inventory_entry.quantity -= adjustment.quantity
    db.commit()
    db.refresh(inventory_entry)
    return inventory_entry


def get_stock_for_item(db: Session, item_id: int) -> list[StockSummaryResponse]:
    """Get stock for one item across all warehouses"""
    _verify_item_exists(db, item_id)

    entries = db.query(Inventory).filter(
        Inventory.item_id == item_id
    ).all()

    return [
        StockSummaryResponse(
            inventory_id=entry.id,
            item_id=entry.item.id,
            item_name=entry.item.name,
            warehouse_id=entry.warehouse.id,
            warehouse_name=entry.warehouse.name,
            warehouse_location=entry.warehouse.location,
            quantity=entry.quantity,
            threshold=entry.threshold,
            last_updated=entry.last_updated
        )
        for entry in entries
    ]


def get_stock_for_warehouse(db: Session, warehouse_id: int) -> list[StockSummaryResponse]:
    """Get all stock in a specific warehouse"""
    _verify_warehouse_exists(db, warehouse_id)

    entries = db.query(Inventory).filter(
        Inventory.warehouse_id == warehouse_id
    ).all()

    return [
        StockSummaryResponse(
            inventory_id=entry.id,
            item_id=entry.item.id,
            item_name=entry.item.name,
            warehouse_id=entry.warehouse.id,
            warehouse_name=entry.warehouse.name,
            warehouse_location=entry.warehouse.location,
            quantity=entry.quantity,
            threshold=entry.threshold,
            last_updated=entry.last_updated
        )
        for entry in entries
    ]


def get_low_stock_alerts(db: Session) -> list[LowStockAlertResponse]:
    """
    Find all inventory entries where quantity is below threshold.
    This is the core of the alert system.
    """
    
    low_stock_entries = db.query(Inventory).filter(
        Inventory.quantity < Inventory.threshold
    ).all()

    return [
        LowStockAlertResponse(
            inventory_id=entry.id,
            item_id=entry.item.id,
            item_name=entry.item.name,
            warehouse_id=entry.warehouse.id,
            warehouse_name=entry.warehouse.name,
            quantity=entry.quantity,
            threshold=entry.threshold,
            
            units_needed=entry.threshold - entry.quantity,
            last_updated=entry.last_updated
        )
        for entry in low_stock_entries
    ]