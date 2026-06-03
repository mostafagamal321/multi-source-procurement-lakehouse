from __future__ import annotations

import json
from pathlib import Path
import pandas as pd
from src.ingestion.common import add_bronze_metadata, ensure_path


def read_purchase_orders(path: str | Path) -> pd.DataFrame:
    with ensure_path(path).open(encoding="utf-8") as fh:
        data = json.load(fh)
    return pd.DataFrame(data["purchase_orders"] if isinstance(data, dict) else data)


def ingest(path: str | Path, pipeline_run_id: str) -> pd.DataFrame:
    return add_bronze_metadata(read_purchase_orders(path), "procurement_erp", "json", Path(path).name, pipeline_run_id)
