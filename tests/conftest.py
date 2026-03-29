# tests/conftest.py

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import Base, get_db

# --- Use a separate SQLite database just for testing ---
# This means tests NEVER touch your real inventory.db
TEST_DATABASE_URL = "sqlite:///./test_inventory.db"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def override_get_db():
    """
    Override the real database with test database.
    FastAPI's dependency injection makes this easy —
    we just swap get_db() with this function during tests.
    """
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def setup_database():
    """
    This runs before EVERY test:
    1. Creates all tables fresh
    2. Runs the test
    3. Drops all tables (clean slate for next test)

    autouse=True means every test gets this automatically.
    """
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    """
    Provides a test HTTP client that:
    - Makes real HTTP requests to your FastAPI app
    - Uses the test database instead of real database
    - No server needs to be running!
    """
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def admin_token(client):
    """
    Creates an admin user and returns their JWT token.
    Reusable across any test that needs admin access.
    """
    # Register admin
    client.post("/auth/register", json={
        "email": "admin@test.com",
        "full_name": "Test Admin",
        "password": "admin123",
        "role": "admin"
    })

    # Login and get token
    response = client.post("/auth/login", json={
        "email": "admin@test.com",
        "password": "admin123"
    })

    return response.json()["access_token"]


@pytest.fixture
def staff_token(client):
    """
    Creates a staff user and returns their JWT token.
    Reusable across any test that needs staff access.
    """
    client.post("/auth/register", json={
        "email": "staff@test.com",
        "full_name": "Test Staff",
        "password": "staff123",
        "role": "staff"
    })

    response = client.post("/auth/login", json={
        "email": "staff@test.com",
        "password": "staff123"
    })

    return response.json()["access_token"]


@pytest.fixture
def admin_headers(admin_token):
    """Returns headers dict with admin JWT token"""
    return {"Authorization": f"Bearer {admin_token}"}


@pytest.fixture
def staff_headers(staff_token):
    """Returns headers dict with staff JWT token"""
    return {"Authorization": f"Bearer {staff_token}"}


@pytest.fixture
def sample_item(client, admin_headers):
    """Creates a sample item and returns it. Reusable in tests."""
    response = client.post("/items/", json={
        "name": "Test Laptop",
        "description": "A test laptop",
        "price": 50000.0,
        "category": "Electronics"
    }, headers=admin_headers)
    return response.json()


@pytest.fixture
def sample_warehouse(client, admin_headers):
    """Creates a sample warehouse and returns it."""
    response = client.post("/warehouses/", json={
        "name": "Test Warehouse",
        "location": "Test Location"
    }, headers=admin_headers)
    return response.json()