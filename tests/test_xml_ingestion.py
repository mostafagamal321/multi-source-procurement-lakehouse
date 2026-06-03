from src.ingestion.ingest_xml import read_suppliers

def test_xml_ingestion(sample_sources):
    df = read_suppliers(sample_sources / "xml" / "suppliers.xml")
    assert df["supplier_id"].tolist() == ["SUP001", "SUP002", "SUP003"]
