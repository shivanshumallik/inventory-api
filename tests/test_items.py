# tests/test_items.py


class TestCreateItem:
    """Tests for POST /items/"""

    def test_admin_can_create_item(self, client, admin_headers):
        """Admin can create a new item"""
        response = client.post("/items/", json={
            "name": "Laptop",
            "description": "Dell XPS",
            "price": 85000.0,
            "category": "Electronics"
        }, headers=admin_headers)

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Laptop"
        assert data["price"] == 85000.0
        assert data["is_active"] == True
        assert "id" in data
        assert "created_at" in data

    def test_staff_cannot_create_item(self, client, staff_headers):
        """Staff user gets 403 when trying to create item"""
        response = client.post("/items/", json={
            "name": "Laptop",
            "price": 85000.0
        }, headers=staff_headers)
        assert response.status_code == 403

    def test_create_item_without_token_fails(self, client):
        """Unauthenticated request returns 401"""
        response = client.post("/items/", json={
            "name": "Laptop",
            "price": 85000.0
        })
        assert response.status_code == 401

    def test_create_item_negative_price_fails(self, client, admin_headers):
        """Negative price is rejected by validation"""
        response = client.post("/items/", json={
            "name": "Laptop",
            "price": -100.0
        }, headers=admin_headers)
        assert response.status_code == 422

    def test_create_item_missing_required_field_fails(self, client, admin_headers):
        """Missing required field returns validation error"""
        response = client.post("/items/", json={
            "name": "Laptop"
            # price is missing — required field
        }, headers=admin_headers)
        assert response.status_code == 422


class TestGetItems:
    """Tests for GET /items/"""

    def test_get_all_items(self, client, admin_headers, sample_item):
        """Authenticated user can get all items"""
        response = client.get("/items/", headers=admin_headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert len(response.json()) == 1

    def test_filter_by_category(self, client, admin_headers):
        """Items can be filtered by category"""
        # Create Electronics item
        client.post("/items/", json={
            "name": "Laptop", "price": 50000, "category": "Electronics"
        }, headers=admin_headers)

        # Create Furniture item
        client.post("/items/", json={
            "name": "Chair", "price": 5000, "category": "Furniture"
        }, headers=admin_headers)

        # Filter for Electronics only
        response = client.get(
            "/items/?category=Electronics",
            headers=admin_headers
        )
        assert response.status_code == 200
        items = response.json()
        assert len(items) == 1
        assert items[0]["category"] == "Electronics"

    def test_filter_by_price_range(self, client, admin_headers):
        """Items can be filtered by price range"""
        client.post("/items/", json={
            "name": "Cheap Item", "price": 500, "category": "Other"
        }, headers=admin_headers)
        client.post("/items/", json={
            "name": "Expensive Item", "price": 100000, "category": "Other"
        }, headers=admin_headers)

        response = client.get(
            "/items/?min_price=1000&max_price=50000",
            headers=admin_headers
        )
        assert response.status_code == 200
        # Only items within range should appear
        for item in response.json():
            assert 1000 <= item["price"] <= 50000

    def test_search_by_name(self, client, admin_headers):
        """Items can be searched by partial name match"""
        client.post("/items/", json={
            "name": "Dell Laptop", "price": 80000, "category": "Electronics"
        }, headers=admin_headers)
        client.post("/items/", json={
            "name": "Office Chair", "price": 8000, "category": "Furniture"
        }, headers=admin_headers)

        response = client.get("/items/?search=dell", headers=admin_headers)
        assert response.status_code == 200
        items = response.json()
        assert len(items) == 1
        assert "Dell" in items[0]["name"]


class TestGetItemById:
    """Tests for GET /items/{item_id}"""

    def test_get_existing_item(self, client, admin_headers, sample_item):
        """Can get an item that exists"""
        item_id = sample_item["id"]
        response = client.get(f"/items/{item_id}", headers=admin_headers)
        assert response.status_code == 200
        assert response.json()["id"] == item_id

    def test_get_nonexistent_item_returns_404(self, client, admin_headers):
        """Getting item with invalid ID returns 404"""
        response = client.get("/items/99999", headers=admin_headers)
        assert response.status_code == 404


class TestUpdateItem:
    """Tests for PUT /items/{item_id}"""

    def test_admin_can_update_item(self, client, admin_headers, sample_item):
        """Admin can update item fields"""
        item_id = sample_item["id"]
        response = client.put(f"/items/{item_id}", json={
            "price": 99000.0
        }, headers=admin_headers)
        assert response.status_code == 200
        assert response.json()["price"] == 99000.0
        # Other fields should be unchanged
        assert response.json()["name"] == sample_item["name"]

    def test_staff_cannot_update_item(self, client, staff_headers, sample_item):
        """Staff cannot update items"""
        item_id = sample_item["id"]
        response = client.put(f"/items/{item_id}", json={
            "price": 99000.0
        }, headers=staff_headers)
        assert response.status_code == 403


class TestDeleteItem:
    """Tests for DELETE /items/{item_id}"""

    def test_admin_can_delete_item(self, client, admin_headers, sample_item):
        """Admin can soft delete an item"""
        item_id = sample_item["id"]
        response = client.delete(f"/items/{item_id}", headers=admin_headers)
        assert response.status_code == 200

        # Item should no longer be accessible
        get_response = client.get(f"/items/{item_id}", headers=admin_headers)
        assert get_response.status_code == 404

    def test_staff_cannot_delete_item(self, client, staff_headers, sample_item):
        """Staff cannot delete items"""
        item_id = sample_item["id"]
        response = client.delete(f"/items/{item_id}", headers=staff_headers)
        assert response.status_code == 403