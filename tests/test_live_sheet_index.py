from fastapi.testclient import TestClient
from app.column_map import SHEET_HEADERS_A_AF
from app.main import app, gateway, sheet_index

client=TestClient(app)

def _row(**overrides):
    headers=list(SHEET_HEADERS_A_AF.values())
    values={h:"" for h in headers}
    values.update(overrides)
    return [values[h] for h in headers]

def test_live_sheet_rebuild_and_search(monkeypatch):
    sheet_index.rows=[]; sheet_index.inverted={}
    monkeypatch.setattr(gateway,'verify_template',lambda:{'ok':True,'mismatches':[]})
    monkeypatch.setattr(gateway,'read_values',lambda a1:[
        _row(EstrategiaId='99335',TareaId='102496',Nombre='Inspección de panel DP con punto caliente',Especialidad='ELEC',Labour1='Electricista Sistema de Potencia'),
        _row(EstrategiaId='99336',TareaId='102497',Nombre='Inspección de banco de baterías',Especialidad='ELEC',Labour1='Servicio Externo Sistema de Potencia'),
    ])
    r=client.post('/index/sheet/rebuild',json={'max_rows':20})
    assert r.status_code==200
    assert r.json()['records']==2
    assert r.json()['write_performed'] is False
    s=client.post('/index/sheet/search',json={'query':'panel punto caliente','top_k':3})
    assert s.status_code==200
    body=s.json()
    assert body['source']=='google_sheet'
    assert body['matches'][0]['EstrategiaId']=='99335'
    assert body['matches'][0]['sheet_row']==5
