import json, subprocess, sys
from pathlib import Path
from app.column_map import REVIEWABLE_COLUMNS
ROOT=Path(__file__).resolve().parents[1]
GEN=ROOT/'pack/02_dataset/generate_semantic_dataset.py'
DATA=ROOT/'pack/outputs/pocket-ai/data/semantic_sheet_matching/dataset_full.json'

def test_generator_real_sheet_columns():
    subprocess.run([sys.executable,str(GEN)],check=True,cwd=ROOT)
    rows=json.loads(DATA.read_text(encoding='utf-8'))
    assert len(rows)==360
    assert {r['target_analysis']['predicted_column_letter'] for r in rows} <= REVIEWABLE_COLUMNS
    assert any(r['target_analysis']['predicted_column_letter']=='J' for r in rows)
    assert any(r['target_analysis']['predicted_column_letter']=='N' for r in rows)
