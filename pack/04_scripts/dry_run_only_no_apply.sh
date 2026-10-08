#!/usr/bin/env bash
set -euo pipefail
echo "Modo seguro: NO escribe en Google Sheets."
echo "Genera propuestas revisables y exige approved=true + ALLOW_SHEET_WRITE=true para aplicar."
echo "La API revalida la cabecera Data!A4:AF4 antes de cada escritura."
