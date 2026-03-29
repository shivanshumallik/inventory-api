# 📦 Inventory & Asset Management API

A production-ready RESTful backend API built with **FastAPI** for managing
inventory items and stock across multiple warehouses.

Built as a portfolio project demonstrating real-world backend engineering practices.

---

## 🚀 Tech Stack

| Technology | Purpose |
|---|---|
| **FastAPI** | Web framework |
| **SQLAlchemy** | ORM for database operations |
| **SQLite** | Database (dev) |
| **Alembic** | Database migrations |
| **Pydantic** | Data validation |
| **JWT (python-jose)** | Authentication |
| **bcrypt (passlib)** | Password hashing |
| **pytest** | Automated testing |

---

## ✨ Features

- 🔐 **JWT Authentication** with role-based access control (Admin/Staff)
- 📦 **Item Management** — full CRUD with filtering, search, pagination
- 🏭 **Multi-Warehouse Support** — track stock per warehouse
- 📊 **Low Stock Alerts** — configurable threshold-based warnings
- 🗄️ **Database Migrations** — Alembic for safe schema changes
- ✅ **Automated Tests** — pytest test suite
- 📝 **Auto-generated Docs** — Swagger UI and ReDoc

---

## 🏗️ Project Structure
```
inventory-api/
├── app/
│   ├── core/
│   │   ├── config.py        # Centralized settings
│   │   ├── database.py      # SQLAlchemy setup
│   │   ├── dependencies.py  # Auth dependencies
│   │   ├── exceptions.py    # Error handling
│   │   └── security.py      # JWT + password hashing
│   ├── models/              # SQLAlchemy DB models
│   ├── schemas/             # Pydantic validation schemas
│   ├── routers/             # API route handlers
│   ├── services/            # Business logic layer
│   └── main.py              # FastAPI application
├── migrations/              # Alembic migrations
├── tests/                   # pytest test suite
├── .env.example             # Environment variable template
└── requirements.txt
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/shivanshumallik/inventory-api.git
cd inventory-api
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment
```bash
cp .env.example .env
# Edit .env with your values
```

### 5. Run database migrations
```bash
alembic upgrade head
```

### 6. Start the server
```bash
uvicorn app.main:app --reload
```

### 7. Open API documentation
```
http://localhost:8000/docs
```

---

## 🔐 Authentication Flow
```
POST /auth/register  →  Create account
POST /auth/login     →  Get JWT token
                         ↓
                    Use token in header:
                    Authorization: Bearer <token>
```

### Role Permissions

| Endpoint | Staff | Admin |
|---|---|---|
| View items | ✅ | ✅ |
| Create/Update/Delete items | ❌ | ✅ |
| View stock | ✅ | ✅ |
| Manage stock | ✅ | ✅ |
| View all users | ❌ | ✅ |

---

## 📡 API Endpoints

### Authentication
```
POST   /auth/register     Register new user
POST   /auth/login        Login and get JWT token
GET    /auth/me           Get current user profile
GET    /auth/users        List all users (Admin only)
```

### Items
```
GET    /items/            List items (with filters)
GET    /items/{id}        Get item by ID
POST   /items/            Create item (Admin only)
PUT    /items/{id}        Update item (Admin only)
DELETE /items/{id}        Delete item (Admin only)
```

### Query Parameters for GET /items/
```
?category=Electronics
?min_price=1000&max_price=50000
?search=laptop
?skip=0&limit=20
```

### Warehouses
```
GET    /warehouses/       List warehouses
GET    /warehouses/{id}   Get warehouse by ID
POST   /warehouses/       Create warehouse (Admin only)
PUT    /warehouses/{id}   Update warehouse (Admin only)
```

### Inventory
```
POST   /inventory/                          Add stock
PUT    /inventory/reduce/{item}/{warehouse} Reduce stock
GET    /inventory/item/{item_id}            Stock by item
GET    /inventory/warehouse/{warehouse_id}  Stock by warehouse
GET    /inventory/low-stock/               Low stock alerts
```

---

## 🧪 Running Tests
```bash
# Run all tests
pytest

# Run with detailed output
pytest -v

# Run specific test file
pytest tests/test_auth.py -v

# Run specific test
pytest tests/test_items.py::TestCreateItem::test_admin_can_create_item -v
```

---

## 👨‍💻 Author

**Shivanshu Raj** — Backend Developer
- GitHub: [@shivanshumallik](https://github.com/shivanshumallik)