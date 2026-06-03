"""Airflow DAG for the Multi-Source Procurement Lakehouse Platform."""
from __future__ import annotations

from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

PROJECT_ROOT = os.getenv("PROJECT_ROOT", "/opt/app")
PYTHONPATH = f"PYTHONPATH={PROJECT_ROOT}"


def publish_pipeline_summary() -> None:
    print("Pipeline completed. Review MinIO, PostgreSQL, dbt artifacts, and reports/data_quality_report.md.")

with DAG(
    dag_id="procurement_lakehouse_pipeline",
    description="Ingest multi-format procurement sources into bronze/silver/gold analytics layers.",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    default_args={"owner": "data-engineering", "retries": 2, "retry_delay": timedelta(minutes=3)},
    tags=["lakehouse", "procurement", "portfolio"],
) as dag:
    wait_for_services = BashOperator(task_id="wait_for_services", bash_command=f"{PYTHONPATH} python {PROJECT_ROOT}/scripts/wait_for_services.py")
    generate_sample_sources = BashOperator(task_id="generate_sample_sources", bash_command=f"{PYTHONPATH} python {PROJECT_ROOT}/scripts/generate_sample_sources.py")
    upload_sources_to_minio_landing = BashOperator(task_id="upload_sources_to_minio_landing", bash_command=f"{PYTHONPATH} python {PROJECT_ROOT}/scripts/upload_sources_to_minio.py")

    ingest_tasks = [
        BashOperator(task_id="ingest_json_purchase_orders", bash_command="echo ingesting JSON purchase orders"),
        BashOperator(task_id="ingest_ndjson_shipments", bash_command="echo ingesting NDJSON shipments"),
        BashOperator(task_id="ingest_xml_suppliers", bash_command="echo ingesting XML suppliers"),
        BashOperator(task_id="ingest_excel_invoices", bash_command="echo ingesting XLSX invoices"),
        BashOperator(task_id="ingest_parquet_inventory", bash_command="echo ingesting Parquet inventory"),
        BashOperator(task_id="ingest_avro_product_catalog", bash_command="echo ingesting Avro products"),
        BashOperator(task_id="ingest_fixed_width_warehouse_records", bash_command="echo ingesting fixed-width warehouse records"),
        BashOperator(task_id="ingest_exchange_rates_api", bash_command="echo ingesting REST API exchange rates"),
    ]
    write_bronze_layer = BashOperator(task_id="write_bronze_layer", bash_command="echo bronze metadata and parquet written by local pipeline task")
    transform_silver_layer = BashOperator(task_id="transform_silver_layer", bash_command=f"{PYTHONPATH} python {PROJECT_ROOT}/scripts/run_local_pipeline.py")
    load_silver_to_postgres = BashOperator(
    task_id="load_silver_to_postgres",
    bash_command=f"{PYTHONPATH} python {PROJECT_ROOT}/scripts/load_silver_to_postgres.py",)
    run_great_expectations = BashOperator(task_id="run_great_expectations", bash_command=f"{PYTHONPATH} python {PROJECT_ROOT}/scripts/run_quality_checks.py")
    run_dbt_build = BashOperator(task_id="run_dbt_build", bash_command=f"cd {PROJECT_ROOT}/dbt && dbt build --profiles-dir .", retries=1)
    generate_quality_report = BashOperator(task_id="generate_quality_report", bash_command="cat /opt/app/reports/data_quality_report.md")
    publish_summary = PythonOperator(task_id="publish_pipeline_summary", python_callable=publish_pipeline_summary)

    wait_for_services >> generate_sample_sources >> upload_sources_to_minio_landing >> ingest_tasks >> write_bronze_layer >> transform_silver_layer >> load_silver_to_postgres >> run_great_expectations >> run_dbt_build >> generate_quality_report >> publish_summary
