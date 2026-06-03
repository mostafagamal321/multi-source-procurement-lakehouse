from __future__ import annotations

from pathlib import Path
import pandas as pd
from fastavro import reader
from src.ingestion.common import add_bronze_metadata, ensure_path


def read_product_catalog(path: str | Path) -> pd.DataFrame:
    with ensure_path(path).open("rb") as fh:
        return pd.DataFrame(list(reader(fh)))


def ingest(path: str | Path, pipeline_run_id: str) -> pd.DataFrame:
    return add_bronze_metadata(read_product_catalog(path), "product_pim", "avro", Path(path).name, pipeline_run_id)
