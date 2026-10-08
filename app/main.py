from __future__ import annotations
import re
from typing import Any
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from .column_map import PROTECTED_COLUMNS, REVIEWABLE_COLUMNS, SHEET_HEADERS_A_AF
from .config import Settings
from .indexer import SemanticIndex
from .sheet_index import LiveSheetIndex
from .sheets import SheetsError, SheetsGateway

app=FastAPI(title="Pocket Test API",version="2.1.0")
settings=Settings(); gateway=SheetsGateway(settings); index=SemanticIndex.load(); sheet_index=LiveSheetIndex()

class Proposal(BaseModel):
    row:int=Field(ge=5); column:str; value:Any; approved:bool=False
class SearchRequest(BaseModel):
    query:str=Field(min_length=3); top_k:int=Field(default=5,ge=1,le=20)
class SheetRebuildRequest(BaseModel):
    max_rows:int=Field(default=996,ge=1,le=996)

@app.get('/health')
def health():
    return {"status":"ok","service":"pocket-test","version":"2.1.0","records_indexed":len(index.records),"live_sheet_records_indexed":len(sheet_index.rows),"sheet_id":settings.spreadsheet_id,"sheet_name":settings.sheet_name,"sheet_auth_mode":settings.auth_mode,"sheet_write_enabled":settings.allow_sheet_write}
@app.get('/index/status')
def index_status(): return {"status":"ready","records":len(index.records),"tokens":len(index.inverted),"source":"validated_package_dataset"}
@app.post('/index/search')
def index_search(item:SearchRequest): return {"query":item.query,"matches":index.search(item.query,item.top_k),"source":"validated_package_dataset"}
@app.get('/index/sheet/status')
def live_sheet_index_status(): return {"status":"ready" if sheet_index.rows else "empty","records":len(sheet_index.rows),"tokens":len(sheet_index.inverted),"source":"google_sheet"}
@app.post('/index/sheet/rebuild')
def rebuild_live_sheet_index(item:SheetRebuildRequest):
    try:
        verification=gateway.verify_template()
        if not verification['ok']:
            raise HTTPException(status_code=409,detail=verification)
        end_row=settings.header_row+item.max_rows
        a1=f"'{settings.sheet_name}'!A{settings.header_row+1}:AF{end_row}"
        values=gateway.read_values(a1)
        count=sheet_index.rebuild(values,start_row=settings.header_row+1)
    except SheetsError as exc:
        raise HTTPException(status_code=502,detail=str(exc)) from exc
    return {"status":"ready","records":count,"range":a1,"source":"google_sheet","write_performed":False}
@app.post('/index/sheet/search')
def live_sheet_search(item:SearchRequest):
    if not sheet_index.rows:
        raise HTTPException(status_code=409,detail='Live Google Sheet index is empty. Call POST /index/sheet/rebuild first.')
    return {"query":item.query,"matches":sheet_index.search(item.query,item.top_k),"source":"google_sheet"}
@app.get('/sheet/verify')
def verify_sheet():
    try: result=gateway.verify_template()
    except SheetsError as exc: raise HTTPException(status_code=502,detail=str(exc)) from exc
    if not result['ok']: raise HTTPException(status_code=409,detail=result)
    return result
@app.post('/proposal')
def proposal(item:Proposal):
    column=item.column.strip().upper()
    if not re.fullmatch(r'[A-Z]{1,2}',column): raise HTTPException(status_code=400,detail='Invalid column')
    if column in PROTECTED_COLUMNS: raise HTTPException(status_code=409,detail=f'Protected column: {column}')
    if column not in REVIEWABLE_COLUMNS: raise HTTPException(status_code=409,detail=f'Column not reviewable in this test: {column}')
    return {"status":"approved" if item.approved else "proposed","row":item.row,"column":column,"header":SHEET_HEADERS_A_AF[column],"value":item.value,"requires_human_approval":not item.approved}
@app.post('/apply')
def apply(item:Proposal):
    if not item.approved: raise HTTPException(status_code=409,detail='Human approval is required before applying a change.')
    column=item.column.strip().upper()
    if column in PROTECTED_COLUMNS or column not in REVIEWABLE_COLUMNS: raise HTTPException(status_code=409,detail=f'Unsafe or non-reviewable column: {column}')
    try:
        verification=gateway.verify_template()
        if not verification['ok']: raise HTTPException(status_code=409,detail=verification)
        result=gateway.update_cell(f'{column}{item.row}',item.value)
    except SheetsError as exc: raise HTTPException(status_code=502,detail=str(exc)) from exc
    return {"status":"applied","cell":f'{column}{item.row}',"google":result}
