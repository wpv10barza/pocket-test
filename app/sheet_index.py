from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field

from .column_map import SHEET_HEADERS_A_AF
from .indexer import _tokens


@dataclass
class LiveSheetIndex:
    rows: list[dict] = field(default_factory=list)
    inverted: dict[str, set[int]] = field(default_factory=dict)

    def rebuild(self, values: list[list[object]], start_row: int = 5) -> int:
        rows: list[dict] = []
        inv: dict[str, set[int]] = defaultdict(set)
        headers = list(SHEET_HEADERS_A_AF.values())
        for offset, raw in enumerate(values):
            padded = list(raw) + [""] * max(0, len(headers) - len(raw))
            if not any(str(v).strip() for v in padded[: len(headers)]):
                continue
            item = {headers[i]: padded[i] for i in range(len(headers))}
            item["_sheet_row"] = start_row + offset
            doc = " ".join(str(item[h]) for h in headers if item[h] not in (None, ""))
            idx = len(rows)
            rows.append(item)
            for token in _tokens(doc):
                inv[token].add(idx)
        self.rows = rows
        self.inverted = dict(inv)
        return len(rows)

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        q = _tokens(query)
        if not q or not self.rows:
            return []
        candidates: set[int] = set()
        for token in q:
            candidates |= self.inverted.get(token, set())
        scored: list[tuple[float, int, dict]] = []
        for idx in candidates:
            item = self.rows[idx]
            doc = _tokens(" ".join(str(v) for k, v in item.items() if not k.startswith("_") and v not in (None, "")))
            score = len(q & doc) / max(1, len(q))
            if score:
                scored.append((score, idx, item))
        scored.sort(key=lambda x: (-x[0], x[1]))
        return [
            {
                "score": round(score, 4),
                "sheet_row": item["_sheet_row"],
                "EstrategiaId": item.get("EstrategiaId", ""),
                "TareaId": item.get("TareaId", ""),
                "Nombre": item.get("Nombre", ""),
                "Especialidad": item.get("Especialidad", ""),
                "Labour1": item.get("Labour1", ""),
            }
            for score, _, item in scored[:top_k]
        ]
