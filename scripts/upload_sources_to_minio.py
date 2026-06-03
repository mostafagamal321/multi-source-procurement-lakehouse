#!/usr/bin/env python
from __future__ import annotations

from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from src.utils.minio_client import ensure_buckets, upload_file

if __name__ == "__main__":
    ensure_buckets()
    for path in (ROOT / "sample_data").rglob("*"):
        if path.is_file():
            upload_file("landing", str(path.relative_to(ROOT / "sample_data")), path)
            print(f"Uploaded {path}")
