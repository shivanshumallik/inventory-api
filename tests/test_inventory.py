# tests/test_inventory.py


class TestStockManagement:
    """Tests for inventory stock operations"""

    def test_add_stock_to_warehouse(
        self, client, admin_headers, sample_item, sample_warehouse
    ):
        """Can add stock for an item in a warehouse"""
        response = client.post("/inventory/", json={
            "item_id": sample_item["id"],
            "warehouse_id": sample_warehouse["id"],
            "quantity": 50,
            "threshold": 10
        }, headers=admin_headers)

        assert response.status_code == 201
        data = response.json()
        assert data["quantity"] == 50
        assert data["threshold"] == 10

    def test_adding_stock_twice_accumulates(
        self, client, admin_headers, sample_item, sample_warehouse
    ):
        """Adding stock twice adds to existing quantity"""
        # Add 30 units
        client.post("/inventory/", json={
            "item_id": sample_item["id"],
            "warehouse_id": sample_warehouse["id"],
            "quantity": 30,
            "threshold": 10
        }, headers=admin_headers)

        # Add 20 more units
        client.post("/inventory/", json={
            "item_id": sample_item["id"],
            "warehouse_id": sample_warehouse["id"],
            "quantity": 20,
            "threshold": 10
        }, headers=admin_headers)

        # Should total 50
        response = client.get(
            f"/inventory/item/{sample_item['id']}",
            headers=admin_headers
        )
        assert response.json()[0]["quantity"] == 50

    def test_reduce_stock(
        self, client, admin_headers, sample_item, sample_warehouse
    ):
        """Can reduce stock from a warehouse"""
        # First add stock
        client.post("/inventory/", json={
            "item_id": sample_item["id"],
            "warehouse_id": sample_warehouse["id"],
            "quantity": 50,
            "threshold": 10
        }, headers=admin_headers)

        # Reduce by 10
        response = client.put(
            f"/inventory/reduce/{sample_item['id']}/{sample_warehouse['id']}",
            json={"quantity": 10},
            headers=admin_headers
        )
        assert response.status_code == 200
        assert response.json()["quantity"] == 40

    def test_reduce_stock_below_zero_fails(
        self, client, admin_headers, sample_item, sample_warehouse
    ):
        """Cannot reduce stock below zero"""
        # Add only 5 units
        client.post("/inventory/", json={
            "item_id": sample_item["id"],
            "warehouse_id": sample_warehouse["id"],
            "quantity": 5,
            "threshold": 10
        }, headers=admin_headers)

        # Try to reduce by 10 (more than available)
        response = client.put(
            f"/inventory/reduce/{sample_item['id']}/{sample_warehouse['id']}",
            json={"quantity": 10},
            headers=admin_headers
        )
        assert response.status_code == 400

    def test_add_stock_invalid_item_fails(
        self, client, admin_headers, sample_warehouse
    ):
        """Adding stock for non-existent item returns 404"""
        response = client.post("/inventory/", json={
            "item_id": 99999,
            "warehouse_id": sample_warehouse["id"],
            "quantity": 50,
            "threshold": 10
        }, headers=admin_headers)
        assert response.status_code == 404


class TestLowStockAlerts:
    """Tests for low stock alert system"""

    def test_low_stock_alert_triggered(
        self, client, admin_headers, sample_item, sample_warehouse
    ):
        """Items below threshold appear in low stock alerts"""
        # Add stock with quantity BELOW threshold
        client.post("/inventory/", json={
            "item_id": sample_item["id"],
            "warehouse_id": sample_warehouse["id"],
            "quantity": 5,   # below threshold
            "threshold": 10
        }, headers=admin_headers)

        response = client.get("/inventory/low-stock/", headers=admin_headers)
        assert response.status_code == 200
        alerts = response.json()
        assert len(alerts) == 1
        assert alerts[0]["item_name"] == sample_item["name"]
        assert alerts[0]["units_needed"] == 5  # 10 - 5

    def test_no_low_stock_when_above_threshold(
        self, client, admin_headers, sample_item, sample_warehouse
    ):
        """Items above threshold don't appear in alerts"""
        # Add stock ABOVE threshold
        client.post("/inventory/", json={
            "item_id": sample_item["id"],
            "warehouse_id": sample_warehouse["id"],
            "quantity": 50,   # well above threshold
            "threshold": 10
        }, headers=admin_headers)

        response = client.get("/inventory/low-stock/", headers=admin_headers)
        assert response.status_code == 200
        assert len(response.json()) == 0

    def test_get_stock_by_item(
        self, client, admin_headers, sample_item, sample_warehouse
    ):
        """Can get stock levels for a specific item"""
        client.post("/inventory/", json={
            "item_id": sample_item["id"],
            "warehouse_id": sample_warehouse["id"],
            "quantity": 25,
            "threshold": 10
        }, headers=admin_headers)

        response = client.get(
            f"/inventory/item/{sample_item['id']}",
            headers=admin_headers
        )
        assert response.status_code == 200
        stock = response.json()
        assert len(stock) == 1
        assert stock[0]["quantity"] == 25
        assert stock[0]["item_name"] == sample_item["name"]