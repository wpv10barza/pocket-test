#!/usr/bin/env python3
from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PATTERNS = {
    "Google access token assignment": re.compile(r"(?im)^\s*GOOGLE_ACCESS_TOKEN\s*=\s*[^\s#][^\r\n]*$"),
    "Google API key assignment": re.compile(r"(?im)^\s*GOOGLE_API_KEY\s*=\s*[^\s#][^\r\n]*$"),
    "Google private key": re.compile(r"-----BEGIN PRIVATE KEY-----"),
}

SKIP_SUFFIXES = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".pdf",
    ".zip", ".gz", ".rar", ".7z", ".bin", ".elf",
}


def tracked_files() -> list[Path]:
    raw = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT)
    return [ROOT / p.decode("utf-8") for p in raw.split(b"\0") if p]


def main() -> None:
    findings: list[str] = []
    for path in tracked_files():
        if path.suffix.lower() in SKIP_SUFFIXES or not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        rel = path.relative_to(ROOT)
        for name, pattern in PATTERNS.items():
            for match in pattern.finditer(text):
                line = text.count("\n", 0, match.start()) + 1
                findings.append(f"{rel}:{line}: {name}")

    if findings:
        print("SECRET_SCAN_FAILED")
        for finding in findings:
            print(f" - {finding}")
        raise SystemExit(1)

    print("SECRET_SCAN_OK")


if __name__ == "__main__":
    main()
