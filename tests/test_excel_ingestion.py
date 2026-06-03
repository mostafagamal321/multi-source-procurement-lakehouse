from src.ingestion.ingest_excel import read_invoices

def test_excel_ingestion(sample_sources):
    df = read_invoices(sample_sources / "excel" / "invoices.xlsx")
    assert "invoice_amount" in df.columns
    assert df["invoice_id"].nunique() == 3
