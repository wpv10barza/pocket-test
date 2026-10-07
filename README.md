# pocket-test

Isolated validation repo for:

`Git repository -> Docker image -> FastAPI -> Google Sheets`

Target: spreadsheet `Estrategias_20260527_2119`, tab `Data`, ID `1tLNo0_xjtmWKM9Y7PcChFut8S0w0kMKeAvFi9zg52gA`.

## Finding from the Pocket-AI pack

The uploaded pack generated 360 synthetic records successfully, but its Python generator used an obsolete A:Q map. The live Sheet header row is:

- I = LimitesAceptables
- J = ComentariosCondicionales
- K = Origen
- L = Frecuencia
- M = UnidadTiempo
- N = Especialidad
- O = Labour1
- P = Labour1Cantidad
- Q = Labour1Horas

This repo fails closed when the live template differs.

The local Excel workbook is intentionally not committed because this repository is public and the workbook contains operational data. Secrets are also excluded.

## WSL / Docker

```bash
cp .env.example .env
docker compose up --build
curl http://localhost:8000/health
curl http://localhost:8000/sheet/verify
```

## Authentication

- `GOOGLE_API_KEY`: read-only verification only when the Sheet is readable without user OAuth.
- `GOOGLE_ACCESS_TOKEN`: private read access and the supported mode for writes.
- An API key alone is not enough for private/write access.

`ALLOW_SHEET_WRITE=false` is the default. `/apply` also requires `approved=true` and re-verifies the A:AF header row before a write.

## Safe proposal test

```bash
curl -X POST http://localhost:8000/proposal \
  -H 'Content-Type: application/json' \
  -d '{"row":5,"column":"J","value":"Prueba controlada","approved":false}'
```

This does not write to Google Sheets.

## Relation to erp-mantto-esp32

`wpv10barza/erp-mantto-esp32` is the firmware/device-contract repository. Its Device API tests transport and human confirmation. Google Sheets persistence is intentionally outside the firmware repo, so this repository isolates the spreadsheet adapter without changing firmware `main`.
