from src.ingestion.ingest_ndjson import read_shipment_events

def test_ndjson_ingestion(sample_sources):
    df = read_shipment_events(sample_sources / "ndjson" / "shipment_events.ndjson")
    assert len(df) == 3
    assert df.loc[0, "shipment_id"] == "SHP001"
