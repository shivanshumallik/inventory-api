# app/core/database.py

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# --- Load environment variables from the .env file ---
# Without this line, os.getenv() below would return None.
load_dotenv()

# --- Read the database URL from the environment ---
# Using an environment variable means you can swap databases
# (SQLite → PostgreSQL) just by changing the .env file.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./inventory.db")

# --- Create the SQLAlchemy engine ---
# The engine is the actual connection to your database.
# connect_args is SQLite-specific: it allows multiple threads
# to use the same connection (needed for FastAPI's async behavior).
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# --- Create a session factory ---
# A "session" is like a temporary workspace where you stage
# database operations before committing them.
# autocommit=False: changes aren't saved until you explicitly call .commit()
# autoflush=False: SQLAlchemy won't auto-send SQL before queries
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- Create the declarative base ---
# All your database models (tables) will inherit from this Base class.
# SQLAlchemy uses it to track which classes represent database tables.
Base = declarative_base()


# --- Dependency function for getting a database session ---
# FastAPI uses "dependency injection" — routes can declare that they
# need a database session, and FastAPI calls this function to provide one.
# The "yield" makes this a generator: code after yield runs on cleanup.
# This guarantees the session is always closed, even if an error occurs.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()