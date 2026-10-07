from fastapi.testclient import TestClient

from app.column_map import SHEET_HEADERS_A_AF, validate_header_row
from app.main import app

client = TestClient(app)


def test_header_map_matches_live_verified_template():
    headers = list(SHEET_HEADERS_A_AF.values())
    assert validate_header_row(headers) == []


def test_health_is_safe_by_default():
    body = client.get("/health").json()
    assert body["status"] == "ok"
    assert body["sheet_write_enabled"] is False


def test_protected_id_column_is_rejected():
    response = client.post("/proposal", json={"row": 5, "column": "A", "value": "999", "approved": False})
    assert response.status_code == 409


def test_reviewable_column_can_be_proposed():
    response = client.post("/proposal", json={"row": 5, "column": "J", "value": "Revisar desviación", "approved": False})
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "proposed"
    assert body["header"] == "ComentariosCondicionales"
    assert body["requires_human_approval"] is True


def test_apply_requires_human_approval_before_network_call():
    response = client.post("/apply", json={"row": 5, "column": "J", "value": "x", "approved": False})
    assert response.status_code == 409
