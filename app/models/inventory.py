# app/models/inventory.py

from sqlalchemy import Column, Integer, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)

    
    item_id = Column(
        Integer,
        ForeignKey("items.id", ondelete="CASCADE"),
        nullable=False
    )

    
    warehouse_id = Column(
        Integer,
        ForeignKey("warehouses.id", ondelete="CASCADE"),
        nullable=False
    )

    
    quantity = Column(Integer, default=0, nullable=False)

    
    last_updated = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    
    __table_args__ = (
        UniqueConstraint("item_id", "warehouse_id", name="unique_item_warehouse"),
    )

    
    item = relationship("Item", back_populates="inventory_entries")
    warehouse = relationship("Warehouse", back_populates="inventory_entries")