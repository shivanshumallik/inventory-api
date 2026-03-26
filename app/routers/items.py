# app/routers/items.py

from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.schemas.item import ItemCreate, ItemUpdate, ItemResponse
from app.services import item_service

router = APIRouter()


@router.get("/", response_model=List[ItemResponse])
def get_items(
    skip: int = Query(default=0, ge=0, description="Records to skip"),
    limit: int = Query(default=100, le=100, description="Max records to return"),
    category: Optional[str] = Query(default=None, description="Filter by category"),
    min_price: Optional[float] = Query(default=None, ge=0, description="Minimum price"),
    max_price: Optional[float] = Query(default=None, ge=0, description="Maximum price"),
    search: Optional[str] = Query(default=None, description="Search by name"),
    db: Session = Depends(get_db)
):
    """
    Get all items with optional filters.
    All query parameters are optional and can be combined.
    """
    return item_service.get_all_items(
        db,
        skip=skip,
        limit=limit,
        category=category,
        min_price=min_price,
        max_price=max_price,
        search=search
    )


@router.get("/{item_id}", response_model=ItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):
    """Get a specific item by ID"""
    return item_service.get_item_by_id(db, item_id)


@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    """Create a new inventory item"""
    return item_service.create_item(db, item)


@router.put("/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, item: ItemUpdate, db: Session = Depends(get_db)):
    """Update an existing item"""
    return item_service.update_item(db, item_id, item)


@router.delete("/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    """Soft delete an item"""
    return item_service.delete_item(db, item_id)