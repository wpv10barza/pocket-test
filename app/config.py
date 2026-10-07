from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    spreadsheet_id: str = os.getenv("SPREADSHEET_ID", "1tLNo0_xjtmWKM9Y7PcChFut8S0w0kMKeAvFi9zg52gA")
    sheet_name: str = os.getenv("SHEET_NAME", "Data")
    header_row: int = int(os.getenv("HEADER_ROW", "4"))
    google_api_key: str = os.getenv("GOOGLE_API_KEY", "")
    google_access_token: str = os.getenv("GOOGLE_ACCESS_TOKEN", "")
    allow_sheet_write: bool = os.getenv("ALLOW_SHEET_WRITE", "false").lower() == "true"

    @property
    def auth_mode(self) -> str:
        if self.google_access_token:
            return "oauth_bearer"
        if self.google_api_key:
            return "api_key_read_only"
        return "unconfigured"
