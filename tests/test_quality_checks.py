import pandas as pd
from src.quality.checks import validate_entity


def test_quality_checks_reject_bad_purchase_order():
    df = pd.DataFrame([
        {"po_id": "PO1", "supplier_id": "S1", "order_date": "2026-01-01", "expected_delivery_date": "2026-01-02", "currency": "USD", "total_amount": 10, "status": "APPROVED"},
        {"po_id": "PO2", "supplier_id": "S1", "order_date": "2026-01-03", "expected_delivery_date": "2026-01-01", "currency": "USD", "total_amount": -1, "status": "APPROVED"},
    ])
    accepted, rejected, result = validate_entity(df, "purchase_orders", ["po_id"], "run", "json")
    assert len(accepted) == 1
    assert len(rejected) == 1
    assert result.score == 50.0


def test_rejected_records_logic():
    df = pd.DataFrame([{"invoice_id": "INV1", "invoice_amount": -2, "invoice_status": "BAD"}])
    _, rejected, _ = validate_entity(df, "invoices", ["invoice_id"], "run", "xlsx")
    assert "invoice_amount < 0" in rejected.loc[0, "rejection_reason"]
    assert "invoice_status outside accepted values" in rejected.loc[0, "rejection_reason"]
