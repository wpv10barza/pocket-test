# Pocket-AI Linux/WSL package (validated adapter)

Contenido importado del ZIP original y corregido contra la hoja real `Estrategias_20260527_2119`.

Cambios de seguridad/compatibilidad:

- La plantilla real usa encabezado en `Data!A4:AF4`.
- `ComentariosCondicionales = J`, `Especialidad = N`, `Labour1 = O`, `Labour1Cantidad = P`, `Labour1Horas = Q`.
- El dataset solo predice columnas revisables: `F,I,J,L,M,N,O,P,Q`.
- No se versiona el XLSX operativo en este repositorio público. Use el Google Sheet real o una copia local fuera de Git.
- Ninguna credencial se guarda en el repositorio.

Generar/validar dataset:

```bash
chmod +x 04_scripts/train_and_prepare_linux.sh
./04_scripts/train_and_prepare_linux.sh
```

Salida: `outputs/pocket-ai/data/semantic_sheet_matching/` y `status=VALIDATED_OK`.
