SHEET_HEADERS_A_AF = {
    "A": "EstrategiaId",
    "B": "ItemMantenible",
    "C": "ModoDeFalla",
    "D": "TipoEstrategia",
    "E": "TareaId",
    "F": "Nombre",
    "G": "TipoTarea",
    "H": "Restriccion",
    "I": "LimitesAceptables",
    "J": "ComentariosCondicionales",
    "K": "Origen",
    "L": "Frecuencia",
    "M": "UnidadTiempo",
    "N": "Especialidad",
    "O": "Labour1",
    "P": "Labour1Cantidad",
    "Q": "Labour1Horas",
    "R": "Labour2",
    "S": "Labour2Cantidad",
    "T": "Labour2Horas",
    "U": "Labour3",
    "V": "Labour3Cantidad",
    "W": "Labour3Horas",
    "X": "Labour4",
    "Y": "Labour4Cantidad",
    "Z": "Labour4Horas",
    "AA": "LabourOtras",
    "AB": "OrigTL1",
    "AC": "OrigTL2",
    "AD": "OrigTL3",
    "AE": "OrigTL4",
    "AF": "Eliminar",
}

REVIEWABLE_COLUMNS = {"F", "I", "J", "L", "M", "N", "O", "P", "Q"}
PROTECTED_COLUMNS = {"A", "E", "AB", "AC", "AD", "AE", "AF"}


def validate_header_row(values: list[str]) -> list[str]:
    mismatches: list[str] = []
    for idx, (letter, header) in enumerate(SHEET_HEADERS_A_AF.items()):
        actual = values[idx] if idx < len(values) else ""
        if str(actual).strip() != header:
            mismatches.append(f"{letter}: expected {header!r}, got {actual!r}")
    return mismatches
