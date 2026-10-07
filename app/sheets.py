from __future__ import annotations

import json
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass

from .column_map import validate_header_row
from .config import Settings


class SheetsError(RuntimeError):
    pass


@dataclass
class SheetsGateway:
    settings: Settings

    def _request(self, method: str, url: str, payload: dict | None = None) -> dict:
        headers = {"Accept": "application/json"}
        if self.settings.google_access_token:
            headers["Authorization"] = f"Bearer {self.settings.google_access_token}"
        data = None
        if payload is not None:
            data = json.dumps(payload).encode("utf-8")
            headers["Content-Type"] = "application/json"
        req = urllib.request.Request(url, data=data, method=method, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                raw = response.read().decode("utf-8")
                return json.loads(raw) if raw else {}
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise SheetsError(f"Google Sheets HTTP {exc.code}: {detail[:500]}") from exc
        except urllib.error.URLError as exc:
            raise SheetsError(f"Google Sheets network error: {exc.reason}") from exc

    def _values_url(self, a1_range: str) -> str:
        escaped = urllib.parse.quote(a1_range, safe="!:'")
        base = f"https://sheets.googleapis.com/v4/spreadsheets/{self.settings.spreadsheet_id}/values/{escaped}"
        if self.settings.google_access_token:
            return base
        if not self.settings.google_api_key:
            raise SheetsError("Configure GOOGLE_API_KEY for public/read-only access or GOOGLE_ACCESS_TOKEN for private/read-write access.")
        return f"{base}?key={urllib.parse.quote(self.settings.google_api_key)}"

    def read_values(self, a1_range: str) -> list[list[object]]:
        result = self._request("GET", self._values_url(a1_range))
        return result.get("values", [])

    def verify_template(self) -> dict:
        a1 = f"'{self.settings.sheet_name}'!A{self.settings.header_row}:AF{self.settings.header_row}"
        values = self.read_values(a1)
        header = values[0] if values else []
        mismatches = validate_header_row([str(v) for v in header])
        return {
            "ok": not mismatches,
            "spreadsheet_id": self.settings.spreadsheet_id,
            "sheet_name": self.settings.sheet_name,
            "header_row": self.settings.header_row,
            "auth_mode": self.settings.auth_mode,
            "mismatches": mismatches,
        }

    def update_cell(self, cell: str, value: object) -> dict:
        if not self.settings.allow_sheet_write:
            raise SheetsError("Sheet writes are disabled. Set ALLOW_SHEET_WRITE=true only after human approval.")
        if not self.settings.google_access_token:
            raise SheetsError("Writes require GOOGLE_ACCESS_TOKEN; an API key alone is not sufficient.")
        a1 = f"'{self.settings.sheet_name}'!{cell}"
        url = self._values_url(a1) + "?valueInputOption=USER_ENTERED"
        return self._request("PUT", url, {"range": a1, "majorDimension": "ROWS", "values": [[value]]})
