from __future__ import annotations

from pathlib import Path
import xml.etree.ElementTree as ET
import pandas as pd
from src.ingestion.common import add_bronze_metadata, ensure_path


def read_suppliers(path: str | Path) -> pd.DataFrame:
    root = ET.parse(ensure_path(path)).getroot()
    rows = []
    for supplier in root.findall("supplier"):
        rows.append({child.tag: child.text for child in supplier})
    return pd.DataFrame(rows)


def ingest(path: str | Path, pipeline_run_id: str) -> pd.DataFrame:
    return add_bronze_metadata(read_suppliers(path), "supplier_mdm", "xml", Path(path).name, pipeline_run_id)
