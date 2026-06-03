from src.ingestion.ingest_fixed_width import read_warehouse_legacy_records

def test_fixed_width_ingestion(sample_sources):
    df = read_warehouse_legacy_records(sample_sources / "fixed_width" / "warehouse_legacy_records.txt")
    assert df.loc[0, "warehouse_id"] == "WH001"
    assert df.loc[0, "product_id"] == "PRD001"
