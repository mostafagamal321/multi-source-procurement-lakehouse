#!/usr/bin/env python
"""Generate realistic multi-format procurement source files."""
from __future__ import annotations

import json
from pathlib import Path
import sys
import pandas as pd
from fastavro import writer, parse_schema

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def main() -> None:
    base = ROOT / "sample_data"
    for sub in ["json", "ndjson", "xml", "excel", "parquet", "avro", "fixed_width"]:
        (base / sub).mkdir(parents=True, exist_ok=True)

    purchase_orders = [
        {"po_id": "PO1001", "supplier_id": "SUP001", "order_date": "2026-01-05", "expected_delivery_date": "2026-01-15", "currency": "USD", "total_amount": 12500.50, "status": "approved"},
        {"po_id": "PO1002", "supplier_id": "SUP002", "order_date": "2026-01-11", "expected_delivery_date": "2026-01-21", "currency": "EUR", "total_amount": 8300.00, "status": "closed"},
        {"po_id": "PO1003", "supplier_id": "SUP003", "order_date": "2026-02-03", "expected_delivery_date": "2026-02-20", "currency": "GBP", "total_amount": 17400.75, "status": "approved"},
        {"po_id": "PO_BAD", "supplier_id": "SUP004", "order_date": "2026-02-10", "expected_delivery_date": "2026-02-01", "currency": "USD", "total_amount": -50, "status": "approved"},
    ]
    (base / "json" / "purchase_orders.json").write_text(json.dumps({"purchase_orders": purchase_orders}, indent=2), encoding="utf-8")

    shipments = [
        {"shipment_id": "SHP001", "po_id": "PO1001", "warehouse_id": "WH001", "shipment_status": "delivered", "event_timestamp": "2026-01-14T10:00:00Z", "carrier": "DHL", "delay_reason": None},
        {"shipment_id": "SHP002", "po_id": "PO1002", "warehouse_id": "WH002", "shipment_status": "delayed", "event_timestamp": "2026-01-25T16:30:00Z", "carrier": "FedEx", "delay_reason": "customs"},
        {"shipment_id": "SHP003", "po_id": "PO1003", "warehouse_id": "WH001", "shipment_status": "in_transit", "event_timestamp": "2026-02-12T08:15:00Z", "carrier": "UPS", "delay_reason": None},
    ]
    (base / "ndjson" / "shipment_events.ndjson").write_text("\n".join(json.dumps(r) for r in shipments) + "\n", encoding="utf-8")

    suppliers_xml = """<suppliers>
  <supplier><supplier_id>SUP001</supplier_id><supplier_name>Acme Industrial</supplier_name><country>US</country><payment_terms>NET30</payment_terms><reliability_score>94.5</reliability_score><created_at>2025-01-01</created_at><updated_at>2026-01-01</updated_at></supplier>
  <supplier><supplier_id>SUP002</supplier_id><supplier_name>Euro Parts GmbH</supplier_name><country>DE</country><payment_terms>NET45</payment_terms><reliability_score>88.2</reliability_score><created_at>2025-02-01</created_at><updated_at>2026-01-10</updated_at></supplier>
  <supplier><supplier_id>SUP003</supplier_id><supplier_name>Britannia Components</supplier_name><country>GB</country><payment_terms>NET30</payment_terms><reliability_score>79.0</reliability_score><created_at>2025-03-01</created_at><updated_at>2026-02-01</updated_at></supplier>
</suppliers>"""
    (base / "xml" / "suppliers.xml").write_text(suppliers_xml, encoding="utf-8")

    invoices = pd.DataFrame([
        {"invoice_id": "INV001", "po_id": "PO1001", "supplier_id": "SUP001", "invoice_date": "2026-01-16", "due_date": "2026-02-15", "paid_date": "2026-02-10", "invoice_amount": 12500.50, "currency": "USD", "invoice_status": "paid"},
        {"invoice_id": "INV002", "po_id": "PO1002", "supplier_id": "SUP002", "invoice_date": "2026-01-22", "due_date": "2026-03-08", "paid_date": None, "invoice_amount": 8300.00, "currency": "EUR", "invoice_status": "overdue"},
        {"invoice_id": "INV003", "po_id": "PO1003", "supplier_id": "SUP003", "invoice_date": "2026-02-21", "due_date": "2026-03-23", "paid_date": None, "invoice_amount": 17400.75, "currency": "GBP", "invoice_status": "open"},
    ])
    with pd.ExcelWriter(base / "excel" / "invoices.xlsx", engine="openpyxl") as xw:
        invoices.to_excel(xw, sheet_name="invoices", index=False)

    pd.DataFrame([
        {"snapshot_date": "2026-02-28", "warehouse_id": "WH001", "product_id": "PRD001", "quantity_on_hand": 120, "reorder_level": 50},
        {"snapshot_date": "2026-02-28", "warehouse_id": "WH001", "product_id": "PRD002", "quantity_on_hand": 20, "reorder_level": 75},
        {"snapshot_date": "2026-02-28", "warehouse_id": "WH002", "product_id": "PRD003", "quantity_on_hand": 300, "reorder_level": 100},
    ]).to_parquet(base / "parquet" / "inventory_snapshot.parquet", index=False)

    schema = parse_schema({"name": "Product", "type": "record", "fields": [
        {"name": "product_id", "type": "string"}, {"name": "product_name", "type": "string"}, {"name": "category", "type": "string"},
        {"name": "unit_cost", "type": "double"}, {"name": "supplier_id", "type": "string"}, {"name": "active_flag", "type": "boolean"},
        {"name": "created_at", "type": "string"}, {"name": "updated_at", "type": "string"}
    ]})
    products = [
        {"product_id": "PRD001", "product_name": "Hydraulic Pump", "category": "MRO", "unit_cost": 250.0, "supplier_id": "SUP001", "active_flag": True, "created_at": "2025-01-01", "updated_at": "2026-01-01"},
        {"product_id": "PRD002", "product_name": "Valve Assembly", "category": "Direct Materials", "unit_cost": 120.0, "supplier_id": "SUP002", "active_flag": True, "created_at": "2025-02-01", "updated_at": "2026-01-10"},
        {"product_id": "PRD003", "product_name": "Safety Sensor", "category": "Electronics", "unit_cost": 80.0, "supplier_id": "SUP003", "active_flag": True, "created_at": "2025-03-01", "updated_at": "2026-02-01"},
    ]
    with (base / "avro" / "product_catalog.avro").open("wb") as fh:
        writer(fh, schema, products)

    records = [("WH001", "PRD001", "STK0000001", "A01B02", "2026-02-28"), ("WH001", "PRD002", "STK0000002", "A01B03", "2026-02-28"), ("WH002", "PRD003", "STK0000003", "C10D04", "2026-02-28")]
    (base / "fixed_width" / "warehouse_legacy_records.txt").write_text("".join(f"{w:<5}{p:<6}{s:<10}{b:<8}{d:<10}\n" for w, p, s, b, d in records), encoding="utf-8")
    print(f"Generated sample sources under {base}")


if __name__ == "__main__":
    main()
