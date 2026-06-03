from __future__ import annotations

import json
import os
import re
from datetime import date, datetime

import pandas as pd
import psycopg2
from psycopg2 import sql
from psycopg2.extras import execute_values


DATASETS = {
    "suppliers": [
        {
            "supplier_id": "SUP001",
            "supplier_name": "Nile Office Supplies",
            "country": "Egypt",
            "payment_terms": "NET30",
            "reliability_score": 92,
            "created_at": "2026-06-01",
            "updated_at": "2026-06-01",
        },
        {
            "supplier_id": "SUP002",
            "supplier_name": "Delta Electronics",
            "country": "UAE",
            "payment_terms": "NET45",
            "reliability_score": 88,
            "created_at": "2026-06-01",
            "updated_at": "2026-06-01",
        },
        {
            "supplier_id": "SUP003",
            "supplier_name": "Global Packaging Co",
            "country": "Turkey",
            "payment_terms": "NET30",
            "reliability_score": 79,
            "created_at": "2026-06-01",
            "updated_at": "2026-06-01",
        },
    ],
    "products": [
        {
            "product_id": "PRD001",
            "product_name": "Office Chair",
            "category": "Furniture",
            "unit_cost": 120.00,
            "supplier_id": "SUP001",
            "active_flag": True,
            "created_at": "2026-06-01",
            "updated_at": "2026-06-01",
        },
        {
            "product_id": "PRD002",
            "product_name": "Laptop Docking Station",
            "category": "Electronics",
            "unit_cost": 180.00,
            "supplier_id": "SUP002",
            "active_flag": True,
            "created_at": "2026-06-01",
            "updated_at": "2026-06-01",
        },
        {
            "product_id": "PRD003",
            "product_name": "Shipping Box",
            "category": "Packaging",
            "unit_cost": 2.50,
            "supplier_id": "SUP003",
            "active_flag": True,
            "created_at": "2026-06-01",
            "updated_at": "2026-06-01",
        },
    ],
    "purchase_orders": [
        {
            "po_id": "PO001",
            "supplier_id": "SUP001",
            "order_date": "2026-06-01",
            "expected_delivery_date": "2026-06-08",
            "currency": "USD",
            "total_amount": 2400.00,
            "status": "APPROVED",
        },
        {
            "po_id": "PO002",
            "supplier_id": "SUP002",
            "order_date": "2026-06-02",
            "expected_delivery_date": "2026-06-10",
            "currency": "EUR",
            "total_amount": 5400.00,
            "status": "APPROVED",
        },
        {
            "po_id": "PO003",
            "supplier_id": "SUP003",
            "order_date": "2026-06-03",
            "expected_delivery_date": "2026-06-12",
            "currency": "USD",
            "total_amount": 800.00,
            "status": "CLOSED",
        },
    ],
    "invoices": [
        {
            "invoice_id": "INV001",
            "po_id": "PO001",
            "supplier_id": "SUP001",
            "invoice_date": "2026-06-04",
            "due_date": "2026-07-04",
            "paid_date": "2026-06-20",
            "invoice_amount": 2400.00,
            "currency": "USD",
            "invoice_status": "PAID",
        },
        {
            "invoice_id": "INV002",
            "po_id": "PO002",
            "supplier_id": "SUP002",
            "invoice_date": "2026-06-05",
            "due_date": "2026-07-20",
            "paid_date": None,
            "invoice_amount": 5400.00,
            "currency": "EUR",
            "invoice_status": "OPEN",
        },
        {
            "invoice_id": "INV003",
            "po_id": "PO003",
            "supplier_id": "SUP003",
            "invoice_date": "2026-06-06",
            "due_date": "2026-07-06",
            "paid_date": None,
            "invoice_amount": 800.00,
            "currency": "USD",
            "invoice_status": "OPEN",
        },
    ],
    "shipments": [
        {
            "shipment_id": "SHP001",
            "po_id": "PO001",
            "warehouse_id": "WH001",
            "shipment_status": "DELIVERED",
            "event_timestamp": "2026-06-08 10:00:00",
            "carrier": "DHL",
            "delay_reason": None,
        },
        {
            "shipment_id": "SHP002",
            "po_id": "PO002",
            "warehouse_id": "WH002",
            "shipment_status": "IN_TRANSIT",
            "event_timestamp": "2026-06-09 13:30:00",
            "carrier": "Aramex",
            "delay_reason": None,
        },
        {
            "shipment_id": "SHP003",
            "po_id": "PO003",
            "warehouse_id": "WH001",
            "shipment_status": "DELAYED",
            "event_timestamp": "2026-06-11 09:15:00",
            "carrier": "FedEx",
            "delay_reason": "Customs delay",
        },
    ],
    "inventory": [
        {
            "snapshot_date": "2026-06-01",
            "warehouse_id": "WH001",
            "product_id": "PRD001",
            "quantity_on_hand": 40,
            "reorder_level": 10,
        },
        {
            "snapshot_date": "2026-06-01",
            "warehouse_id": "WH002",
            "product_id": "PRD002",
            "quantity_on_hand": 15,
            "reorder_level": 8,
        },
        {
            "snapshot_date": "2026-06-01",
            "warehouse_id": "WH001",
            "product_id": "PRD003",
            "quantity_on_hand": 300,
            "reorder_level": 100,
        },
    ],
    "exchange_rates": [
        {
            "rate_date": "2026-06-01",
            "from_currency": "USD",
            "to_currency": "EGP",
            "exchange_rate": 47.5,
        },
        {
            "rate_date": "2026-06-01",
            "from_currency": "EUR",
            "to_currency": "EGP",
            "exchange_rate": 51.2,
        },
        {
            "rate_date": "2026-06-01",
            "from_currency": "GBP",
            "to_currency": "EGP",
            "exchange_rate": 60.1,
        },
    ],
}


def get_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "postgres-warehouse"),
        port=int(os.getenv("POSTGRES_PORT", "5432")),
        dbname=os.getenv("POSTGRES_DB", "procurement"),
        user=os.getenv("POSTGRES_USER", "procurement"),
        password=os.getenv("POSTGRES_PASSWORD", "procurement"),
    )


def sanitize_column_name(col: object) -> str:
    name = str(col).strip().lower()
    name = re.sub(r"[^a-z0-9_]+", "_", name)
    name = re.sub(r"_+", "_", name).strip("_")
    return name or "unknown_column"


def clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [sanitize_column_name(col) for col in df.columns]
    return df


def normalize_value(value):
    if pd.isna(value):
        return None

    if isinstance(value, (datetime, date)):
        return value.isoformat()

    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False)

    return value


def create_table(conn, schema_name: str, table_name: str, columns: list[str]) -> None:
    column_defs = [sql.SQL("{} TEXT").format(sql.Identifier(col)) for col in columns]

    with conn.cursor() as cur:
        cur.execute(sql.SQL("CREATE SCHEMA IF NOT EXISTS {}").format(sql.Identifier(schema_name)))
        cur.execute(sql.SQL("DROP TABLE IF EXISTS {}.{} CASCADE").format(sql.Identifier(schema_name), sql.Identifier(table_name)))
        cur.execute(
            sql.SQL("CREATE TABLE {}.{} ({})").format(
                sql.Identifier(schema_name),
                sql.Identifier(table_name),
                sql.SQL(", ").join(column_defs),
            )
        )


def load_dataframe(conn, schema_name: str, table_name: str, df: pd.DataFrame) -> None:
    df = clean_columns(df)

    columns = list(df.columns)
    create_table(conn, schema_name, table_name, columns)

    rows = [
        tuple(normalize_value(row[col]) for col in columns)
        for _, row in df.iterrows()
    ]

    insert_sql = sql.SQL("INSERT INTO {}.{} ({}) VALUES %s").format(
        sql.Identifier(schema_name),
        sql.Identifier(table_name),
        sql.SQL(", ").join(sql.Identifier(col) for col in columns),
    )

    with conn.cursor() as cur:
        execute_values(cur, insert_sql.as_string(conn), rows, page_size=1000)

    print(f"Loaded {schema_name}.{table_name}: {len(df)} rows")


def create_rejected_records_table(conn) -> None:
    df = pd.DataFrame(
        [
            {
                "source_name": "purchase_orders",
                "source_file_type": "JSON",
                "record_identifier": "PO_BAD_001",
                "rejection_reason": "Negative total_amount",
                "raw_payload": '{"po_id":"PO_BAD_001","total_amount":-100}',
                "rejected_at": "2026-06-01 12:00:00",
                "pipeline_run_id": "manual_load",
            }
        ]
    )
    load_dataframe(conn, "audit", "rejected_records", df)


def main() -> None:
    conn = get_connection()

    try:
        for table_name, records in DATASETS.items():
            df = pd.DataFrame(records)
            load_dataframe(conn, "staging", table_name, df)

        create_rejected_records_table(conn)

        conn.commit()
        print("Warehouse staging load completed successfully.")
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()