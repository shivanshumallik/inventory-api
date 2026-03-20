from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

# This class represents the 'items' table in SQLite.
# Every attribute = one column in the table.
# SQLAlchemy reads this class and knows exactly how to create the table.
class Item(Base):
    # __tablename__ tells SQLAlchemy what to name the table in the database.
    # Convention: lowercase, plural of the model name.
    __tablename__ = "items"

    # Primary key — every table needs one.
    # index=True makes lookups by ID faster (SQLAlchemy creates a DB index).
    id = Column(Integer, primary_key=True, index=True)

    # name is required (nullable=False means it CANNOT be empty).
    # index=True because we'll often search/filter by name.
    name = Column(String, nullable=False, index=True)

    # description is optional — nullable=True means it CAN be empty.
    description = Column(String, nullable=True)

    # quantity defaults to 0 if not provided.
    quantity = Column(Integer, default=0, nullable=False)

    # price can have decimal points (e.g., 29.99).
    price = Column(Float, nullable=False)

    # category helps group items. Optional.
    category = Column(String, nullable=True)

    # is_active is our soft-delete flag.
    # Default is True — every new item is active by default.
    is_active = Column(Boolean, default=True, nullable=False)

    # created_at is set automatically when the row is first inserted.
    # server_default=func.now() means the DATABASE sets this timestamp.
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # updated_at is updated automatically every time the row changes.
    # onupdate=func.now() means SQLAlchemy updates this on every save.
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())