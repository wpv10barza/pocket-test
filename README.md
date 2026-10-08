# pocket-test — Pocket-AI CI/CD validation

Repositorio aislado para validar dos cadenas complementarias:

`ZIP Pocket-AI → dataset/index → FastAPI → Docker`

`FastAPI → Google Sheets (lectura) → índice live`

El `main` de `wpv10barza/erp-mantto-esp32` se usa como referencia de contrato/ejecución, pero no se modifica desde este repositorio.

## Estado corregido del Sheet

Google Sheet: `Estrategias_20260527_2119`

- pestaña: `Data`
- cabecera: fila `4`
- rango de plantilla: `A:AF`
- columnas revisables: `F,I,J,L,M,N,O,P,Q`
- columnas protegidas: `A,E,AB,AC,AD,AE,AF`

La versión original del ZIP tenía un mapeo A:Q obsoleto. Esta rama corrige, entre otros, `ComentariosCondicionales=J` y `Especialidad=N`.

## WSL: clonar y ejecutar

```bash
git clone https://github.com/wpv10barza/pocket-test.git
cd pocket-test
cp .env.example .env
# coloque una credencial de lectura válida solo en .env; nunca haga git add .env
docker compose up --build -d
curl http://localhost:8000/health
curl http://localhost:8000/index/status
curl -X POST http://localhost:8000/index/search \
  -H 'Content-Type: application/json' \
  -d '{"query":"termografía punto caliente tablero","top_k":3}'
curl http://localhost:8000/sheet/verify
```

Para indexar las filas reales del Google Sheet en memoria, sin escribir:

```bash
curl -X POST http://localhost:8000/index/sheet/rebuild \
  -H 'Content-Type: application/json' \
  -d '{"max_rows":996}'
curl http://localhost:8000/index/sheet/status
curl -X POST http://localhost:8000/index/sheet/search \
  -H 'Content-Type: application/json' \
  -d '{"query":"panel distribución punto caliente","top_k":5}'
```

`/index/sheet/rebuild` primero verifica que `Data!A4:AF4` siga siendo la plantilla esperada y después solo lee `A5:AF1000`. Devuelve `write_performed=false`.

Para actualizar un checkout existente:

```bash
cd ~/pocket-test
git switch main
git pull --ff-only origin main
cp -n .env.example .env
docker compose up --build -d
```

## Autenticación de Google Sheets

- `GOOGLE_API_KEY`: lectura únicamente cuando Google permite acceder al Sheet con API key (por ejemplo, datos públicos/compatibles con ese modo).
- `GOOGLE_ACCESS_TOKEN`: lectura privada y modo admitido para escritura autorizada.
- `ALLOW_SHEET_WRITE=false` por defecto.
- `/apply` exige `approved=true`, vuelve a verificar `Data!A4:AF4` y recién después intenta escribir.
- El XLSX operativo del ZIP no se publica porque el repositorio es público.

## Sin Docker

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/validate_package.py
pytest -q
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## CI/CD

`.github/workflows/ci-cd.yml` ejecuta:

1. generador del ZIP corregido (360 registros);
2. validación del mapeo real;
3. pruebas API/index;
4. `docker build`;
5. smoke test del contenedor;
6. en `main`, publicación a `ghcr.io/wpv10barza/pocket-test:latest`.

La CI no guarda credenciales de Google. La prueba live se ejecuta en WSL con `.env` o mediante credenciales gestionadas fuera del repositorio.
