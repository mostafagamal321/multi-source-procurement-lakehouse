from __future__ import annotations

from pathlib import Path
import pandas as pd
from src.ingestion.common import add_bronze_metadata, ensure_path

WIDTHS = [5, 6, 10, 8, 10]
COLUMNS = ["warehouse_id", "product_id", "legacy_stock_code", "bin_location", "last_count_date"]


def read_warehouse_legacy_records(path: str | Path) -> pd.DataFrame:
    return pd.read_fwf(ensure_path(path), widths=WIDTHS, names=COLUMNS, dtype=str)


def ingest(path: str | Path, pipeline_run_id: str) -> pd.DataFrame:
    return add_bronze_metadata(read_warehouse_legacy_records(path), "legacy_wms", "fixed_width_txt", Path(path).name, pipeline_run_id)
