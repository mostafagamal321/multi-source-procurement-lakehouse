from __future__ import annotations

import json
from pathlib import Path
import pandas as pd
from src.ingestion.common import add_bronze_metadata, ensure_path


def read_shipment_events(path: str | Path) -> pd.DataFrame:
    rows = [json.loads(line) for line in ensure_path(path).read_text(encoding="utf-8").splitlines() if line.strip()]
    return pd.DataFrame(rows)


def ingest(path: str | Path, pipeline_run_id: str) -> pd.DataFrame:
    return add_bronze_metadata(read_shipment_events(path), "carrier_events", "ndjson", Path(path).name, pipeline_run_id)
