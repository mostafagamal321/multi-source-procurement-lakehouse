"""Shared ingestion helpers."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def record_hash(record: dict[str, Any]) -> str:
    payload = json.dumps(record, sort_keys=True, default=str)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def add_bronze_metadata(df: pd.DataFrame, source_system: str, source_file_type: str, source_file_name: str, pipeline_run_id: str) -> pd.DataFrame:
    out = df.copy()
    now = utc_now()
    records = out.to_dict(orient="records")
    out.insert(0, "source_system", source_system)
    out.insert(1, "source_file_type", source_file_type)
    out.insert(2, "source_file_name", source_file_name)
    out.insert(3, "ingestion_timestamp", now)
    out.insert(4, "raw_record_hash", [record_hash(r) for r in records])
    out.insert(5, "pipeline_run_id", pipeline_run_id)
    out.insert(6, "loaded_at", now)
    return out


def ensure_path(path: str | Path) -> Path:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(p)
    return p
