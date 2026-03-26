# app/services/item_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate


def get_all_items(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    category: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    search: str | None = None,
) -> list[Item]:
    """
    Get all active items with optional filtering and search.
    Every filter is optional — only applied if the user provides it.
    """
    
    query = db.query(Item).filter(Item.is_active == True)

    
    if category:
        query = query.filter(Item.category == category)

    
    if min_price is not None:
        query = query.filter(Item.price >= min_price)

    
    if max_price is not None:
        query = query.filter(Item.price <= max_price)

    
    if search:
        query = query.filter(Item.name.ilike(f"%{search}%"))

    
    return query.offset(skip).limit(limit).all()


def get_item_by_id(db: Session, item_id: int) -> Item:
    """Get a single item or raise 404"""
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


def create_item(db: Session, item_data: ItemCreate) -> Item:
    """Create a new item"""
    db_item = Item(**item_data.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_item(db: Session, item_id: int, item_data: ItemUpdate) -> Item:
    """Update only the fields that were provided"""
    db_item = get_item_by_id(db, item_id)
    update_data = item_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_item, field, value)
    db.commit()
    db.refresh(db_item)
    return db_item


def delete_item(db: Session, item_id: int) -> dict:
    """Soft delete an item"""
    db_item = get_item_by_id(db, item_id)
    db_item.is_active = False
    db.commit()
    return {"message": f"Item '{db_item.name}' has been deactivated successfully"}