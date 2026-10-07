#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.column_map import SHEET_HEADERS_A_AF

EXPECTED_CORE = {
    "F": "Nombre",
    "I": "LimitesAceptables",
    "J": "ComentariosCondicionales",
    "L": "Frecuencia",
    "M": "UnidadTiempo",
    "N": "Especialidad",
    "O": "Labour1",
    "P": "Labour1Cantidad",
    "Q": "Labour1Horas",
}

for col, header in EXPECTED_CORE.items():
    actual = SHEET_HEADERS_A_AF[col]
    assert actual == header, f"{col}: {actual} != {header}"

print("VALIDATED_OK")
print("Core column map matches the verified Data sheet header row.")
