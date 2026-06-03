from __future__ import annotations

from pathlib import Path
import pandas as pd
from src.ingestion.common import add_bronze_metadata, ensure_path


def read_invoices(path: str | Path) -> pd.DataFrame:
    return pd.read_excel(ensure_path(path), sheet_name="invoices")


def ingest(path: str | Path, pipeline_run_id: str) -> pd.DataFrame:
    return add_bronze_metadata(read_invoices(path), "accounts_payable", "xlsx", Path(path).name, pipeline_run_id)
