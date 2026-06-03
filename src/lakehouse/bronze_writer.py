"""Bronze writer for landing-source dataframes."""
from __future__ import annotations

from pathlib import Path
import pandas as pd
from src.utils.config import get_settings


def write_bronze_dataset(df: pd.DataFrame, dataset_name: str, pipeline_run_id: str) -> Path:
    settings = get_settings()
    target = settings.lakehouse_dir / "bronze" / dataset_name / f"pipeline_run_id={pipeline_run_id}"
    target.mkdir(parents=True, exist_ok=True)
    output = target / "part-00000.parquet"
    df.to_parquet(output, index=False)
    return output


def write_many(datasets: dict[str, pd.DataFrame], pipeline_run_id: str) -> dict[str, Path]:
    return {name: write_bronze_dataset(df, name, pipeline_run_id) for name, df in datasets.items()}
