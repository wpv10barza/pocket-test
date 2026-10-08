# pocket-test — Pocket-AI validation and CI/CD

Repositorio aislado para validar:

`Pocket-AI package → dataset/index → FastAPI → Docker → Google Sheets`

y, cuando se configura una credencial de lectura:

`Google Sheets → índice live read-only → búsqueda`.

El repositorio `wpv10barza/erp-mantto-esp32` conserva el contrato del dispositivo y se mantiene separado de la persistencia de Google Sheets.

## Google Sheet validado

- Spreadsheet: `Estrategias_20260527_2119`
- ID: `1tLNo0_xjtmWKM9Y7PcChFut8S0w0kMKeAvFi9zg52gA`
- Pestaña: `Data`
- Cabecera: fila `4`
- Plantilla: `A:AF`
- Revisables: `F,I,J,L,M,N,O,P,Q`
- Protegidas: `A,E,AB,AC,AD,AE,AF`

El adaptador usa fail-closed: antes de una escritura vuelve a verificar `Data!A4:AF4`. Si la plantilla no coincide, la operación se rechaza.

## Ejecución WSL / Linux

```bash
git clone https://github.com/wpv10barza/pocket-test.git
cd pocket-test
cp .env.example .env
nano .env
docker compose up --build -d
```

Verificación:

```bash
curl -sS http://localhost:8000/health | jq
curl -sS http://localhost:8000/index/status | jq
curl -sS -X POST http://localhost:8000/index/search \
  -H 'Content-Type: application/json' \
  -d '{"query":"termografía punto caliente tablero","top_k":3}' | jq
```

## Indexación read-only del Google Sheet

Con una credencial de lectura válida en `.env`:

```bash
curl -sS http://localhost:8000/sheet/verify | jq

curl -sS -X POST http://localhost:8000/index/sheet/rebuild \
  -H 'Content-Type: application/json' \
  -d '{"max_rows":996}' | jq

curl -sS -X POST http://localhost:8000/index/sheet/search \
  -H 'Content-Type: application/json' \
  -d '{"query":"panel distribución punto caliente","top_k":5}' | jq
```

`/index/sheet/rebuild` solo lee datos y devuelve `write_performed=false`.

## Escritura controlada

Por defecto:

```dotenv
ALLOW_SHEET_WRITE=false
```

Para escribir se requieren simultáneamente:

- `GOOGLE_ACCESS_TOKEN` válido;
- `ALLOW_SHEET_WRITE=true`;
- solicitud `/apply` con `approved=true`;
- plantilla `Data!A4:AF4` sin cambios;
- columna incluida en el conjunto revisable.

Una API key nunca habilita escritura.

## CI/CD

Existe un único workflow: `.github/workflows/ci-cd.yml`.

En cada Pull Request y push ejecuta:

1. compilación de todos los módulos Python;
2. generación y validación de los 360 registros Pocket-AI;
3. escaneo de secretos versionados;
4. pruebas unitarias/API;
5. construcción de Docker;
6. smoke test de `/health`, índice y búsqueda;
7. prueba fail-closed de `/apply`;
8. comprobación de que la imagen no contiene credenciales Google.

Solo en un push exitoso a `main`, después de todas las pruebas, publica:

```text
ghcr.io/wpv10barza/pocket-test:latest
ghcr.io/wpv10barza/pocket-test:<commit-sha>
```

El job de pruebas tiene únicamente `contents: read`. El permiso `packages: write` existe exclusivamente en el job de publicación.

## Pruebas locales sin Docker

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/check_repo_security.py
python scripts/validate_package.py
pytest -q
```

No versionar `.env`, tokens OAuth, claves API, JSON de service account ni claves privadas.
