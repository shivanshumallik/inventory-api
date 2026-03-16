# app/routers/items.py

from fastapi import APIRouter

# --- Create a router instance ---
# This is like a mini FastAPI app. We define routes on it,
# then register it in main.py with app.include_router().
router = APIRouter()


# --- A simple test endpoint ---
# GET /items/ will return this response.
# Later, this will query the database and return real items.
@router.get("/")
def get_items():
    return [
        {"id": 1, "name": "Laptop", "quantity": 10},
        {"id": 2, "name": "Monitor", "quantity": 5},
    ]


# --- A route with a path parameter ---
# GET /items/1 will return the item with id=1.
# The {item_id} in the path becomes a function argument.
# FastAPI automatically validates that it's an integer.
@router.get("/{item_id}")
def get_item(item_id: int):
    return {"id": item_id, "name": "Laptop", "quantity": 10}
