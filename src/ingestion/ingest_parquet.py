from __future__ import annotations

from pathlib import Path
import pandas as pd
from src.ingestion.common import add_bronze_metadata, ensure_path


def read_inventory(path: str | Path) -> pd.DataFrame:
    return pd.read_parquet(ensure_path(path))


def ingest(path: str | Path, pipeline_run_id: str) -> pd.DataFrame:
    return add_bronze_metadata(read_inventory(path), "warehouse_wms", "parquet", Path(path).name, pipeline_run_id)
