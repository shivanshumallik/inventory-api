# app/models/warehouse.py

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Warehouse(Base):
    __tablename__ = "warehouses"

    id = Column(Integer, primary_key=True, index=True)

    
    name = Column(String, nullable=False, index=True)

    
    location = Column(String, nullable=False)

   
    is_active = Column(Boolean, default=True, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

   
    inventory_entries = relationship("Inventory", back_populates="warehouse")