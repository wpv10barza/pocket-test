from __future__ import annotations

import pytest

from app.config import Settings
from app.sheets import SheetsError, SheetsGateway


def make_settings(**overrides):
    values = {
        "spreadsheet_id": "sheet-id",
        "sheet_name": "Data",
        "header_row": 4,
        "google_api_key": "",
        "google_access_token": "",
        "allow_sheet_write": False,
    }
    values.update(overrides)
    return Settings(**values)


def test_auth_mode_unconfigured():
    assert make_settings().auth_mode == "unconfigured"


def test_auth_mode_api_key_is_read_only():
    assert make_settings(google_api_key="test-key").auth_mode == "api_key_read_only"


def test_auth_mode_oauth_bearer_has_priority():
    settings = make_settings(google_api_key="test-key", google_access_token="token")
    assert settings.auth_mode == "oauth_bearer"


def test_read_requires_some_google_credential():
    gateway = SheetsGateway(make_settings())
    with pytest.raises(SheetsError, match="Configure GOOGLE_API_KEY"):
        gateway.read_values("'Data'!A4:AF4")


def test_update_is_blocked_when_write_flag_is_false():
    gateway = SheetsGateway(make_settings(google_access_token="token"))
    with pytest.raises(SheetsError, match="Sheet writes are disabled"):
        gateway.update_cell("J5", "blocked")


def test_update_requires_oauth_even_when_write_flag_is_true():
    gateway = SheetsGateway(
        make_settings(google_api_key="read-key", allow_sheet_write=True)
    )
    with pytest.raises(SheetsError, match="Writes require GOOGLE_ACCESS_TOKEN"):
        gateway.update_cell("J5", "blocked")


def test_template_verification_fails_closed_on_header_mismatch(monkeypatch):
    gateway = SheetsGateway(make_settings(google_api_key="read-key"))
    monkeypatch.setattr(
        gateway,
        "read_values",
        lambda _a1: [["EstrategiaId", "WRONG_HEADER"]],
    )
    result = gateway.verify_template()
    assert result["ok"] is False
    assert result["mismatches"]
    assert any("B:" in mismatch for mismatch in result["mismatches"])
