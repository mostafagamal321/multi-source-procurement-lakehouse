# Architecture

Raw procurement sources are generated locally, optionally uploaded to MinIO `landing`, converted into metadata-rich Bronze Parquet, standardized into Silver Parquet, loaded to PostgreSQL `staging`, modeled by dbt into `marts`, and queried by Superset. Airflow orchestrates the DAG and Jenkins validates CI/CD.

```mermaid
flowchart LR
  A[JSON/NDJSON/XML/XLSX/Parquet/Avro/TXT/API] --> B[MinIO Landing]
  B --> C[Bronze Parquet]
  C --> D[Silver Parquet + Rejected]
  D --> E[PostgreSQL staging/audit]
  E --> F[dbt Gold Marts]
  F --> G[Superset Dashboard]
  D --> H[Great Expectations Data Docs + Reports]
  I[Airflow] --> B
  I --> C
  I --> D
  I --> E
  I --> F
  J[Jenkins] --> I
```
