# REGLAS DE CONTROL PARA EDITAR EL SHEET

## Principio
No se edita `Data` directamente durante entrenamiento o pruebas.

## Estados permitidos
- PROPUESTO
- EN_REVISION
- APROBADO
- RECHAZADO
- APLICADO
- ERROR

## Campos de control recomendados
Usar `05_control_templates/Control_MLDev_template.csv`.

## Columnas inicialmente editables con aprobación
- F Nombre
- I LimitesAceptables
- J ComentariosCondicionales
- L Frecuencia
- M UnidadTiempo
- N Especialidad
- O Labour1
- P Labour1Cantidad
- Q Labour1Horas

## Columnas protegidas
- A EstrategiaId
- E TareaId
- AB OrigTL1
- AC OrigTL2
- AD OrigTL3
- AE OrigTL4
- AF Eliminar

Estas columnas no se modifican sin fuente oficial o instrucción humana explícita.
