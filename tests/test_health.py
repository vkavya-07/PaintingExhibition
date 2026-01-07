def test_health_endpoint(client):
    r = client.get("/health/")
    assert r.status_code == 200
    data = r.json()
    assert data.get("status") == "ok"
    assert "uptime" in data
    assert isinstance(data["uptime"], (int, float))