# Multi-Source Procurement Data Lakehouse Platform

A production-style local data engineering portfolio project that ingests procurement and supply-chain data from JSON, NDJSON, XML, Excel XLSX, Parquet, Avro, fixed-width TXT, and REST API JSON sources into a Bronze/Silver/Gold lakehouse architecture.

## Business Problem

Procurement teams receive fragmented data from ERP, supplier MDM, accounts payable, carriers, warehouse systems, product catalogs, and currency-rate providers. This platform unifies those sources to answer spend, delay, inventory risk, source quality, rejection, and exchange-rate impact questions.

## Why This Project Matters

The project demonstrates real data engineering skills: multi-format ingestion, S3-compatible object storage, metadata-rich Bronze files, quality-gated Silver datasets, rejected-record handling, PostgreSQL warehousing, dbt marts, orchestration, CI/CD, and dashboard-ready SQL.

## Why It Is Not a Basic CSV ETL Project

CSV is intentionally not a core source. The main inputs are JSON, NDJSON, XML, XLSX, Parquet, Avro, fixed-width TXT, and REST API JSON. The repository includes Airflow, MinIO, Great Expectations-style checks, dbt, Superset, Jenkins, Docker Compose, tests, and professional documentation.


## Tech Stack

Python, pandas, pyarrow, fastavro, openpyxl, requests, SQLAlchemy/psycopg2, MinIO, PostgreSQL, Apache Airflow, dbt, Great Expectations expectations, Apache Superset, Jenkins, Docker Compose, pytest, and ruff.

## Source File Types

| Business data | File/API | Format | Ingestion module |
|---|---|---|---|
| Purchase orders | `purchase_orders.json` | JSON | `src/ingestion/ingest_json.py` |
| Shipment events | `shipment_events.ndjson` | NDJSON | `src/ingestion/ingest_ndjson.py` |
| Suppliers | `suppliers.xml` | XML | `src/ingestion/ingest_xml.py` |
| Invoices | `invoices.xlsx` | Excel XLSX | `src/ingestion/ingest_excel.py` |
| Inventory | `inventory_snapshot.parquet` | Parquet | `src/ingestion/ingest_parquet.py` |
| Products | `product_catalog.avro` | Avro | `src/ingestion/ingest_avro.py` |
| Legacy warehouse | `warehouse_legacy_records.txt` | Fixed-width TXT | `src/ingestion/ingest_fixed_width.py` |
| FX rates | public API or mock | REST API JSON | `src/ingestion/ingest_exchange_rates_api.py` |

## Data Flow

1. Generate realistic sample sources.
2. Optionally upload raw files to MinIO `landing`.
3. Ingest each source type into Bronze Parquet with source metadata and record hashes.
4. Transform Bronze into Silver standardized datasets.
5. Route invalid records to rejected records instead of crashing the pipeline.
6. Load Silver datasets to PostgreSQL `staging` and rejected records to `audit`.
7. Run dbt to create Gold dimensions, facts, and marts in `marts`.
8. Query marts from Superset.

## Bronze, Silver, and Gold

- **Bronze** keeps original fields plus `source_system`, `source_file_type`, `source_file_name`, `ingestion_timestamp`, `raw_record_hash`, `pipeline_run_id`, and `loaded_at`.
- **Silver** standardizes names, casts dates and numerics, uppercases statuses/currencies, de-duplicates business keys, adds `dq_passed`, and writes rejected records.
- **Gold** is created by dbt marts for spend, supplier performance, delivery performance, inventory risk, and data quality reporting.

## Airflow Orchestration

The DAG `procurement_lakehouse_pipeline` is manually triggerable, uses retries and retry delays, reads environment variables, and contains tasks for service waiting, source generation/upload, each source ingestion type, Bronze/Silver processing, warehouse loading, Great Expectations/custom checks, dbt build, reporting, and summary publication.

## Data Quality and Great Expectations

Custom pandas quality checks validate non-null business keys, numeric ranges, date ordering, allowed invoice and shipment statuses, duplicate keys, row counts, rejected counts, freshness, and source-level quality scores. A Great Expectations suite template is included at `great_expectations/expectations/procurement_suite.json` and reports are written to `reports/data_quality_report.json` and `.md`.

## dbt

The dbt project includes staging models, dimensions, facts, analytics marts, schema tests (`not_null`, `unique`, `relationships`, `accepted_values`), descriptions, and a supplier snapshot for slowly changing supplier attributes.

## Superset Dashboard

Superset is included in Docker Compose. Use `sql/superset_dashboard_queries.sql` to create charts for total spend, spend by supplier/category, monthly trends, invoice delays, shipment delays, inventory risk, top delayed suppliers, data quality, rejections, and FX-adjusted cost. Full dashboard automation is intentionally left manual for reliability in local portfolio environments.

## Jenkins CI/CD

The declarative Jenkins pipeline installs dependencies, lints Python, runs unit tests, validates Docker Compose, builds images, starts services, runs smoke tests and quality checks, runs dbt, archives reports/logs, and fails on test or dbt failures.

## Maintainability Features

- Modular ingestion by source type.
- Shared config, logging, MinIO, and database utilities.
- Typed functions and docstrings for important code.
- Config-driven environment variables with `.env.example`.
- Clear documentation and Makefile commands.

## Scalability Features

- S3-compatible MinIO storage.
- Bronze/Silver/Gold layering.
- Parquet storage with partition-style run folders.
- `pipeline_run_id` traceability.
- dbt marts for analytics-ready models.
- Easy pattern for adding more file types.

## Availability Features

- Docker restart policies and persistent volumes.
- Airflow retries.
- Health checks for PostgreSQL and MinIO.
- Bad records are routed to rejected outputs.
- Quality reports and operational logs.

## Local Setup

```bash
cd multi-source-procurement-lakehouse
cp .env.example .env
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

## How to Run

```bash
make generate-sources
make run-pipeline
make up
```

To run the complete platform with Docker:

```bash
make build
make up
```

Then trigger `procurement_lakehouse_pipeline` in Airflow.

## UI URLs

- Airflow: http://localhost:8080
- Superset: http://localhost:8088
- MinIO Console: http://localhost:9001
- Jenkins: http://localhost:8081

Default local usernames/passwords are documented in `.env.example`. Replace them for any non-local environment.

## Tests, Linting, dbt, and Reports

```bash
make test
make lint
make dbt-build
make quality
```

Reports:

- `reports/data_quality_report.json`
- `reports/data_quality_report.md`
- `reports/pipeline_summary.md`

## Screenshot Checklist

See `docs/screenshots_checklist.md`. Recommended screenshots: Airflow DAG graph, MinIO buckets, Superset charts, Jenkins success, quality report, and dbt lineage/docs.

## Portfolio/CV Bullet Points

- Built a local lakehouse platform ingesting eight source formats into Bronze/Silver/Gold layers.
- Implemented data quality gates with rejected-record routing and source-level scores.
- Modeled procurement KPIs with dbt and exposed dashboard SQL for Superset.
- Orchestrated pipelines with Airflow and automated CI/CD with Jenkins.
- Used MinIO and PostgreSQL to simulate cloud object storage and an analytics warehouse.

## Troubleshooting

See `docs/troubleshooting.md`. Common issues are missing Python dependencies, occupied ports, Docker socket permissions for Jenkins, and unavailable public exchange-rate APIs. Keep `OFFLINE_API_MODE=true` for deterministic tests.

## Known Limitations

- Superset dashboard creation is documented through SQL rather than fully automated.
- The local pipeline uses pandas/Parquet for junior-friendly execution; Spark can be added as a future enhancement.
- The public exchange API is optional and mock mode is the default for offline reliability.
