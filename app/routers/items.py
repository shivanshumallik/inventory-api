# app/routers/items.py

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.item import ItemCreate, ItemUpdate, ItemResponse
from app.services import item_service

router = APIRouter()


# --- GET all items ---
# Response is a list of ItemResponse objects.
# db: Session = Depends(get_db) is dependency injection —
# FastAPI calls get_db() automatically and passes the session here.
@router.get("/", response_model=List[ItemResponse])
def get_items(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Retrieve all active inventory items."""
    return item_service.get_all_items(db, skip=skip, limit=limit)


# --- GET item by ID ---
@router.get("/{item_id}", response_model=ItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):
    """Retrieve a single item by ID."""
    return item_service.get_item_by_id(db, item_id)


# --- CREATE item ---
# status_code=201 means "Created" — more accurate than default 200 "OK"
@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    """Create a new inventory item."""
    return item_service.create_item(db, item)


# --- UPDATE item ---
@router.put("/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, item: ItemUpdate, db: Session = Depends(get_db)):
    """Update an existing item (partial update supported)."""
    return item_service.update_item(db, item_id, item)


# --- DELETE item (soft delete) ---
@router.delete("/{item_id}", status_code=status.HTTP_200_OK)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    """Soft delete an item (marks as inactive)."""
    return item_service.delete_item(db, item_id)
