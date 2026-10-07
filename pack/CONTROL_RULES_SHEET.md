# Control rules

`Data` is read-only during training and proposal generation.

A write is allowed only after human approval, only to a reviewable column, and only after the live header row still matches the verified A:AF template.

Reviewable in this isolated test: `F`, `I`, `J`, `L`, `M`, `N`, `O`, `P`, `Q`.

Protected: `A` (EstrategiaId), `E` (TareaId), `AB:AE` (OrigTL1..4), `AF` (Eliminar).

The repository never stores Google/Gemini API keys or OAuth access tokens.
