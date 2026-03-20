# app/services/item_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate


def get_all_items(db: Session, skip: int = 0, limit: int = 100) -> list[Item]:
    """
    Retrieve all active items from the database.
    skip and limit enable pagination — don't return 10,000 rows at once.
    """
    return db.query(Item).filter(Item.is_active == True).offset(skip).limit(limit).all()


def get_item_by_id(db: Session, item_id: int) -> Item:
    """
    Retrieve a single item by its ID.
    Raises a 404 error if the item doesn't exist or is inactive.
    """
    item = db.query(Item).filter(Item.id == item_id, Item.is_active == True).first()

    # If no item found, raise an HTTP 404 error.
    # FastAPI catches HTTPException and returns it as a proper JSON error response.
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found"
        )
    return item


def create_item(db: Session, item_data: ItemCreate) -> Item:
    """
    Create a new item in the database.
    """
    # Convert the Pydantic schema into a SQLAlchemy model instance.
    # model_dump() turns the Pydantic object into a plain dictionary.
    # **dict unpacks it as keyword arguments to Item().
    db_item = Item(**item_data.model_dump())

    db.add(db_item)       # Stage the new item (not saved yet)
    db.commit()           # Actually write to the database
    db.refresh(db_item)   # Reload from DB to get generated fields (id, created_at)

    return db_item


def update_item(db: Session, item_id: int, item_data: ItemUpdate) -> Item:
    """
    Update an existing item.
    Only updates fields that were actually provided (partial update).
    """
    # First, verify the item exists
    db_item = get_item_by_id(db, item_id)

    # model_dump(exclude_unset=True) only returns fields the user actually sent.
    # If they only sent {"quantity": 5}, we only update quantity.
    # Without exclude_unset=True, all optional fields would be None
    # and would overwrite existing data!
    update_data = item_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_item, field, value)  # dynamically set each field

    db.commit()
    db.refresh(db_item)
    return db_item


def delete_item(db: Session, item_id: int) -> dict:
    """
    Soft delete an item by setting is_active to False.
    We never actually remove the row from the database.
    """
    db_item = get_item_by_id(db, item_id)

    db_item.is_active = False  # Soft delete
    db.commit()

    return {"message": f"Item '{db_item.name}' has been deactivated successfully"}