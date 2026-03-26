# app/schemas/inventory.py

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class InventoryCreate(BaseModel):
    item_id: int = Field(..., description="ID of the item")
    warehouse_id: int = Field(..., description="ID of the warehouse")
    quantity: int = Field(..., ge=0, description="Initial stock quantity")
    
    threshold: int = Field(default=10, ge=0, description="Low stock warning threshold")


class StockAdjustment(BaseModel):
    quantity: int = Field(..., gt=0, description="Units to add or remove")


class InventoryResponse(BaseModel):
    id: int
    item_id: int
    warehouse_id: int
    quantity: int
    threshold: int
    last_updated: datetime

    class Config:
        from_attributes = True


class StockSummaryResponse(BaseModel):
    inventory_id: int
    item_id: int
    item_name: str
    warehouse_id: int
    warehouse_name: str
    warehouse_location: str
    quantity: int
    threshold: int
    last_updated: datetime



class LowStockAlertResponse(BaseModel):
    inventory_id: int
    item_id: int
    item_name: str
    warehouse_id: int
    warehouse_name: str
    quantity: int
    threshold: int
   
    units_needed: int
    last_updated: datetime