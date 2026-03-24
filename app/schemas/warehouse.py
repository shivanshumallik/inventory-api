# app/schemas/warehouse.py

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class WarehouseCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100,
                      description="Name of the warehouse")
    location: str = Field(..., min_length=1, max_length=200,
                          description="Physical location or address")


class WarehouseUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    location: Optional[str] = Field(None, min_length=1, max_length=200)
    is_active: Optional[bool] = None


class WarehouseResponse(BaseModel):
    id: int
    name: str
    location: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True