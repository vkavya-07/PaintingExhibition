from datetime import datetime, timedelta, timezone
from app.models import Painting

def test_admin_can_add_and_list_paintings(client, session):
    # admin adds a painting
    payload = {"createdBy": "Alice", "size": "24x36", "isAvailableForSale": True, "price": 1000.0}
    r = client.post("/paintings/", json=payload, headers={"x-role": "admin"})
    assert r.status_code == 200
    data = r.json()
    assert data["createdBy"] == "Alice"

    # user lists paintings
    r = client.get("/paintings/", headers={"x-role": "user"})
    assert r.status_code == 200
    lst = r.json()
    assert isinstance(lst, list)
    assert len(lst) == 1

def test_admin_update_put_and_patch(client):
    payload = {"createdBy": "Bob", "size": "18x24", "isAvailableForSale": True, "price": 500.0}
    r = client.post("/paintings/", json=payload, headers={"x-role": "admin"})
    assert r.status_code == 200
    p = r.json()
    pid = p["id"]

    # full replace via PUT
    payload2 = {"createdBy": "Bob", "size": "20x20", "isAvailableForSale": True, "price": 550.0}
    r = client.put(f"/paintings/{pid}", json=payload2, headers={"x-role": "admin"})
    assert r.status_code == 200
    updated = r.json()
    assert updated["size"] == "20x20"

    # patch
    patch = {"price": 600.0}
    r = client.patch(f"/paintings/{pid}", json=patch, headers={"x-role": "admin"})
    assert r.status_code == 200
    patched = r.json()
    assert patched["price"] == 600.0

def test_user_can_buy_painting_and_admin_can_query_sold(client):
    # admin creates painting
    payload = {"createdBy": "Carol", "size": "12x12", "isAvailableForSale": True, "price": 200.0}
    r = client.post("/paintings/", json=payload, headers={"x-role": "admin"})
    p = r.json()
    pid = p["id"]

    soldDate = datetime.now(timezone.utc).isoformat()
    buy_payload = {"soldTo": "Dave", "soldDate": soldDate}
    r = client.patch(f"/paintings/{pid}/buy", json=buy_payload, headers={"x-role": "user"})
    assert r.status_code == 200
    bought = r.json()
    assert bought["soldTo"] == "Dave"
    assert bought["isAvailableForSale"] == False

    # admin query sold
    r = client.get("/paintings/sold", headers={"x-role": "admin"})
    assert r.status_code == 200
    sold = r.json()
    assert any(s["id"] == pid for s in sold)

    # filter by createdBy
    r = client.get("/paintings/sold?createdBy=Carol", headers={"x-role": "admin"})
    assert r.status_code == 200
    sold = r.json()
    assert all(s["createdBy"] == "Carol" for s in sold)