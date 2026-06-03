from src.ingestion.ingest_avro import read_product_catalog

def test_avro_ingestion(sample_sources):
    df = read_product_catalog(sample_sources / "avro" / "product_catalog.avro")
    assert {"product_id", "category", "unit_cost"}.issubset(df.columns)
