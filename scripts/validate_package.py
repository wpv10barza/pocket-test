#!/usr/bin/env python3
import json, subprocess, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from app.column_map import SHEET_HEADERS_A_AF, REVIEWABLE_COLUMNS
from app.indexer import DATASET, GENERATOR, SemanticIndex
EXPECTED={"F":"Nombre","I":"LimitesAceptables","J":"ComentariosCondicionales","L":"Frecuencia","M":"UnidadTiempo","N":"Especialidad","O":"Labour1","P":"Labour1Cantidad","Q":"Labour1Horas"}
assert all(SHEET_HEADERS_A_AF[k]==v for k,v in EXPECTED.items())
assert REVIEWABLE_COLUMNS==set(EXPECTED)
subprocess.run([sys.executable,str(GENERATOR)],check=True)
records=json.loads(DATASET.read_text(encoding='utf-8'))
assert len(records)==360
assert all(r['target_analysis']['predicted_column_letter'] in REVIEWABLE_COLUMNS for r in records)
idx=SemanticIndex.load(); assert len(idx.records)==360
assert idx.search('termografía punto caliente',3)
print('VALIDATED_OK records=360 columns=F,I,J,L,M,N,O,P,Q index=ready')
