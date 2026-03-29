# app/routers/items.py

from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.dependencies import get_current_user, require_admin
from app.schemas.item import ItemCreate, ItemUpdate, ItemResponse
from app.services import item_service
from app.models.user import User

router = APIRouter()


@router.get("/", response_model=List[ItemResponse])
def get_items(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, le=100),
    category: Optional[str] = Query(default=None),
    min_price: Optional[float] = Query(default=None, ge=0),
    max_price: Optional[float] = Query(default=None, ge=0),
    search: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
    # Any logged in user can view items
    current_user: User = Depends(get_current_user)
):
    """Get all items — requires authentication"""
    return item_service.get_all_items(
        db, skip=skip, limit=limit,
        category=category, min_price=min_price,
        max_price=max_price, search=search
    )


@router.get("/{item_id}", response_model=ItemResponse)
def get_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific item — requires authentication"""
    return item_service.get_item_by_id(db, item_id)


@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(
    item: ItemCreate,
    db: Session = Depends(get_db),
    # Only admins can create items
    current_user: User = Depends(require_admin)
):
    """Create a new item — ADMIN ONLY"""
    return item_service.create_item(db, item)


@router.put("/{item_id}", response_model=ItemResponse)
def update_item(
    item_id: int,
    item: ItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Update an item — ADMIN ONLY"""
    return item_service.update_item(db, item_id, item)


@router.delete("/{item_id}")
def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Delete an item — ADMIN ONLY"""
    return item_service.delete_item(db, item_id)