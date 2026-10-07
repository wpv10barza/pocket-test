from __future__ import annotations

import re
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from .column_map import PROTECTED_COLUMNS, REVIEWABLE_COLUMNS, SHEET_HEADERS_A_AF
from .config import Settings
from .sheets import SheetsError, SheetsGateway

app = FastAPI(title="Pocket Test API", version="1.0.0")
settings = Settings()
gateway = SheetsGateway(settings)


class Proposal(BaseModel):
    row: int = Field(ge=5)
    column: str
    value: Any
    approved: bool = False


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "pocket-test",
        "sheet_id": settings.spreadsheet_id,
        "sheet_name": settings.sheet_name,
        "sheet_auth_mode": settings.auth_mode,
        "sheet_write_enabled": settings.allow_sheet_write,
    }


@app.get("/sheet/verify")
def verify_sheet():
    try:
        result = gateway.verify_template()
    except SheetsError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    if not result["ok"]:
        raise HTTPException(status_code=409, detail=result)
    return result


@app.post("/proposal")
def proposal(item: Proposal):
    column = item.column.strip().upper()
    if not re.fullmatch(r"[A-Z]{1,2}", column):
        raise HTTPException(status_code=400, detail="Invalid column")
    if column in PROTECTED_COLUMNS:
        raise HTTPException(status_code=409, detail=f"Protected column: {column}")
    if column not in REVIEWABLE_COLUMNS:
        raise HTTPException(status_code=409, detail=f"Column not reviewable in this test: {column}")
    return {
        "status": "approved" if item.approved else "proposed",
        "row": item.row,
        "column": column,
        "header": SHEET_HEADERS_A_AF[column],
        "value": item.value,
        "requires_human_approval": not item.approved,
    }


@app.post("/apply")
def apply(item: Proposal):
    if not item.approved:
        raise HTTPException(status_code=409, detail="Human approval is required before applying a change.")
    column = item.column.strip().upper()
    if column in PROTECTED_COLUMNS or column not in REVIEWABLE_COLUMNS:
        raise HTTPException(status_code=409, detail=f"Unsafe or non-reviewable column: {column}")
    try:
        verification = gateway.verify_template()
        if not verification["ok"]:
            raise HTTPException(status_code=409, detail=verification)
        result = gateway.update_cell(f"{column}{item.row}", item.value)
    except SheetsError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    return {"status": "applied", "cell": f"{column}{item.row}", "google": result}
