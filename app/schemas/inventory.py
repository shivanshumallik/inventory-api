# app/schemas/inventory.py

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class InventoryCreate(BaseModel):
    item_id: int = Field(..., description="ID of the item")
    warehouse_id: int = Field(..., description="ID of the warehouse")
    quantity: int = Field(..., ge=0, description="Initial stock quantity")


class StockAdjustment(BaseModel):
    # Used for adding or reducing stock
    # quantity is always positive — the operation (add/reduce) is
    # determined by which endpoint you call, not this value
    quantity: int = Field(..., gt=0, description="Units to add or remove")


class InventoryResponse(BaseModel):
    id: int
    item_id: int
    warehouse_id: int
    quantity: int
    last_updated: datetime

    class Config:
        from_attributes = True


class StockSummaryResponse(BaseModel):
    # A richer response that includes item and warehouse names
    # for easier reading in the API response
    inventory_id: int
    item_id: int
    item_name: str
    warehouse_id: int
    warehouse_name: str
    warehouse_location: str
    quantity: int
    last_updated: datetime