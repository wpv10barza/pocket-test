#!/usr/bin/env bash
set -euo pipefail
PACK_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PACK_ROOT"
echo "== Pocket-AI Linux/WSL dataset build =="
command -v python3 >/dev/null 2>&1 || { echo "ERROR: python3 no está instalado"; exit 1; }
python3 02_dataset/generate_semantic_dataset.py
cat outputs/pocket-ai/logs/hailort.log
python3 - <<'PY2'
import json
from pathlib import Path
p=Path('outputs/pocket-ai/data/semantic_sheet_matching/validation_report.json')
r=json.loads(p.read_text(encoding='utf-8'))
assert r['status']=='VALIDATED_OK'
assert r['total_records']==360
print('DATASET_OK records=360')
PY2
