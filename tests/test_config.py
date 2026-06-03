from src.utils.config import get_settings
from src.ingestion.ingest_exchange_rates_api import MOCK_RESPONSE, parse_exchange_rates


def test_config_loading():
    settings = get_settings()
    assert "landing" in settings.buckets
    assert settings.reports_dir.exists()


def test_api_mock_parsing():
    df = parse_exchange_rates(MOCK_RESPONSE, rate_date="2026-06-01")
    assert {"rate_date", "from_currency", "to_currency", "exchange_rate"}.issubset(df.columns)
    assert (df["exchange_rate"] > 0).all()
