#!/usr/bin/env python
"""Run the end-to-end local procurement lakehouse pipeline."""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.ingestion import ingest_avro, ingest_excel, ingest_exchange_rates_api, ingest_fixed_width, ingest_json, ingest_ndjson, ingest_parquet, ingest_xml
from src.lakehouse.bronze_writer import write_many
from src.lakehouse.silver_transformer import transform_datasets, write_silver_many
from src.lakehouse.warehouse_loader import load_silver_to_postgres
from src.quality.report import render_pipeline_summary, render_quality_reports
from src.utils.config import get_settings
from src.utils.logger import get_logger

LOGGER = get_logger(__name__)


def pipeline_run_id() -> str:
    return datetime.now(timezone.utc).strftime("run_%Y%m%d_%H%M%S")


def run_pipeline(load_warehouse: bool = False) -> None:
    settings = get_settings()
    run_id = pipeline_run_id()
    subprocess.run([sys.executable, str(ROOT / "scripts" / "generate_sample_sources.py")], check=True)
    sample = settings.sample_data_dir
    bronze = {
        "bronze_purchase_orders": ingest_json.ingest(sample / "json" / "purchase_orders.json", run_id),
        "bronze_shipment_events": ingest_ndjson.ingest(sample / "ndjson" / "shipment_events.ndjson", run_id),
        "bronze_suppliers": ingest_xml.ingest(sample / "xml" / "suppliers.xml", run_id),
        "bronze_invoices": ingest_excel.ingest(sample / "excel" / "invoices.xlsx", run_id),
        "bronze_inventory": ingest_parquet.ingest(sample / "parquet" / "inventory_snapshot.parquet", run_id),
        "bronze_product_catalog": ingest_avro.ingest(sample / "avro" / "product_catalog.avro", run_id),
        "bronze_warehouse_legacy_records": ingest_fixed_width.ingest(sample / "fixed_width" / "warehouse_legacy_records.txt", run_id),
        "bronze_exchange_rates": ingest_exchange_rates_api.ingest(settings.exchange_api_url, run_id, offline=settings.offline_api_mode),
    }
    bronze_outputs = write_many(bronze, run_id)
    silver, rejected, quality_results = transform_datasets(bronze, run_id)
    silver_outputs = write_silver_many(silver, rejected, run_id)
    if load_warehouse:
        load_silver_to_postgres(silver, rejected)
    render_quality_reports(quality_results, rejected)
    render_pipeline_summary(run_id, bronze_outputs, silver_outputs)
    LOGGER.info("Pipeline %s completed", run_id)


if __name__ == "__main__":
    run_pipeline(load_warehouse="--load-warehouse" in sys.argv)
