#!/usr/bin/env python
from __future__ import annotations

from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts.run_local_pipeline import run_pipeline

if __name__ == "__main__":
    run_pipeline(load_warehouse=False)
