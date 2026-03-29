# app/models/user.py

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.sql import func
from app.core.database import Base
import enum


# Define roles as an Enum
# Enum means only these exact values are allowed — nothing else
class UserRole(str, enum.Enum):
    ADMIN = "admin"    # Full access — create, update, delete
    STAFF = "staff"    # Limited access — read and update stock only


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    # Email is the username — must be unique across all users
    email = Column(String, unique=True, nullable=False, index=True)

    # Full name for display purposes
    full_name = Column(String, nullable=False)

    # NEVER store plain passwords — only the hashed version
    # Even if DB is hacked, hashes can't be reversed easily
    hashed_password = Column(String, nullable=False)

    # Role determines what the user can do
    role = Column(
        Enum(UserRole),
        default=UserRole.STAFF,
        nullable=False
    )

    # Soft disable accounts without deleting them
    is_active = Column(Boolean, default=True, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())