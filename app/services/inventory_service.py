# app/services/inventory_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.inventory import Inventory
from app.models.item import Item
from app.models.warehouse import Warehouse
from app.schemas.inventory import InventoryCreate, StockAdjustment, StockSummaryResponse


def _verify_item_exists(db: Session, item_id: int) -> Item:
    """Internal helper — verify item exists before doing stock operations"""
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
    """Internal helper — verify warehouse exists before doing stock operations"""
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
    """
    Add stock for an item in a warehouse.
    If an entry already exists, ADD to the existing quantity.
    If it doesn't exist, CREATE a new entry.
    """
    # First verify both item and warehouse actually exist
    _verify_item_exists(db, inventory_data.item_id)
    _verify_warehouse_exists(db, inventory_data.warehouse_id)

    # Check if an inventory entry already exists for this item+warehouse
    existing = db.query(Inventory).filter(
        Inventory.item_id == inventory_data.item_id,
        Inventory.warehouse_id == inventory_data.warehouse_id
    ).first()

    if existing:
        # Entry exists — just add to the quantity
        existing.quantity += inventory_data.quantity
        db.commit()
        db.refresh(existing)
        return existing
    else:
        # No entry yet — create a fresh one
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
    """
    Reduce stock for an item in a specific warehouse.
    Cannot reduce below zero — raises error if not enough stock.
    """
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

    # Cannot go below zero — this would be a negative inventory
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
    """
    Get stock levels for a specific item across ALL warehouses.
    Returns a rich response with item and warehouse names.
    """
    _verify_item_exists(db, item_id)

    entries = db.query(Inventory).filter(
        Inventory.item_id == item_id
    ).all()

    # Build a rich response combining data from Item, Warehouse, Inventory
    result = []
    for entry in entries:
        result.append(StockSummaryResponse(
            inventory_id=entry.id,
            item_id=entry.item.id,
            item_name=entry.item.name,
            warehouse_id=entry.warehouse.id,
            warehouse_name=entry.warehouse.name,
            warehouse_location=entry.warehouse.location,
            quantity=entry.quantity,
            last_updated=entry.last_updated
        ))
    return result


def get_stock_for_warehouse(db: Session, warehouse_id: int) -> list[StockSummaryResponse]:
    """
    Get all stock in a specific warehouse across ALL items.
    """
    _verify_warehouse_exists(db, warehouse_id)

    entries = db.query(Inventory).filter(
        Inventory.warehouse_id == warehouse_id
    ).all()

    result = []
    for entry in entries:
        result.append(StockSummaryResponse(
            inventory_id=entry.id,
            item_id=entry.item.id,
            item_name=entry.item.name,
            warehouse_id=entry.warehouse.id,
            warehouse_name=entry.warehouse.name,
            warehouse_location=entry.warehouse.location,
            quantity=entry.quantity,
            last_updated=entry.last_updated
        ))
    return result