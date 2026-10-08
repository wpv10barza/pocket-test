from fastapi.testclient import TestClient
from app.column_map import SHEET_HEADERS_A_AF, validate_header_row
from app.main import app,index
client=TestClient(app)

def test_header_map_matches_live_verified_template(): assert validate_header_row(list(SHEET_HEADERS_A_AF.values()))==[]
def test_health_safe_and_indexed():
    b=client.get('/health').json(); assert b['status']=='ok'; assert b['sheet_write_enabled'] is False; assert b['records_indexed']==360
def test_index_status(): assert client.get('/index/status').json()['records']==360
def test_semantic_search():
    r=client.post('/index/search',json={'query':'termografía punto caliente tablero','top_k':5}); assert r.status_code==200; assert r.json()['matches']; assert any('TERMOGRAF' in m['prt_code'] or 'termograf' in m['query'].lower() for m in r.json()['matches'])
def test_protected_id_column_is_rejected(): assert client.post('/proposal',json={'row':5,'column':'A','value':'999','approved':False}).status_code==409
def test_reviewable_column_can_be_proposed():
    r=client.post('/proposal',json={'row':5,'column':'J','value':'Revisar desviación','approved':False}); assert r.status_code==200; assert r.json()['header']=='ComentariosCondicionales'
def test_apply_requires_human_approval_before_network_call(): assert client.post('/apply',json={'row':5,'column':'J','value':'x','approved':False}).status_code==409
