from src.ingestion.ingest_json import ingest, read_purchase_orders

def test_json_ingestion(sample_sources):
    df = read_purchase_orders(sample_sources / "json" / "purchase_orders.json")
    assert {"po_id", "supplier_id", "total_amount"}.issubset(df.columns)
    bronze = ingest(sample_sources / "json" / "purchase_orders.json", "test_run")
    assert "raw_record_hash" in bronze.columns
