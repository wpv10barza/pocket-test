#!/usr/bin/env python3
from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SELF = Path("scripts/check_repo_security.py")

TOKEN_PATTERNS = {
    "Google API key": re.compile("AI" + "za[0-9A-Za-z_-]{30,}"),
    "GitHub classic token": re.compile("gh" + "p_[A-Za-z0-9]{30,}"),
    "GitHub fine-grained token": re.compile("github_" + "pat_[A-Za-z0-9_]{40,}"),
    "AWS access key id": re.compile("AK" + "IA[0-9A-Z]{16}"),
}

SKIP_SUFFIXES = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".pdf",
    ".zip", ".gz", ".rar", ".7z", ".bin", ".elf",
}


def tracked_files() -> list[Path]:
    raw = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT)
    return [ROOT / p.decode("utf-8") for p in raw.split(b"\0") if p]


def nonempty_assignment(text: str, name: str) -> list[int]:
    hits: list[int] = []
    prefix = name + "="
    for number, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if not stripped.startswith(prefix):
            continue
        value = stripped[len(prefix):].strip()
        if value and not value.startswith("#"):
            hits.append(number)
    return hits


def main() -> None:
    findings: list[str] = []
    for path in tracked_files():
        rel = path.relative_to(ROOT)
        if rel == SELF or path.suffix.lower() in SKIP_SUFFIXES or not path.is_file():
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        for env_name in ("GOOGLE_API_KEY", "GOOGLE_ACCESS_TOKEN"):
            for line in nonempty_assignment(content, env_name):
                findings.append(f"{rel}:{line}: non-empty {env_name}")

        private_key_marker = "-----BEGIN " + "PRIVATE KEY-----"
        if private_key_marker in content:
            line = content.count("\n", 0, content.index(private_key_marker)) + 1
            findings.append(f"{rel}:{line}: private key material")

        for name, pattern in TOKEN_PATTERNS.items():
            for match in pattern.finditer(content):
                line = content.count("\n", 0, match.start()) + 1
                findings.append(f"{rel}:{line}: {name}")

    if findings:
        print("SECRET_SCAN_FAILED")
        for finding in findings:
            print(f" - {finding}")
        raise SystemExit(1)

    print("SECRET_SCAN_OK")


if __name__ == "__main__":
    main()
