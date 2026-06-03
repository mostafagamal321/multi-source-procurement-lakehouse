from __future__ import annotations

from datetime import date
from typing import Any
import pandas as pd
try:
    import requests
except Exception:  # offline fallback for local CI
    requests = None
from src.ingestion.common import add_bronze_metadata

MOCK_RESPONSE = {"base_code": "USD", "time_last_update_utc": "Mon, 01 Jun 2026 00:00:01 +0000", "rates": {"USD": 1.0, "EUR": 0.92, "GBP": 0.78, "EGP": 47.25}}


def parse_exchange_rates(payload: dict[str, Any], rate_date: str | None = None, to_currency: str = "USD") -> pd.DataFrame:
    base = payload.get("base_code") or payload.get("base") or "USD"
    rates = payload.get("rates", {})
    rows = []
    business_date = rate_date or date.today().isoformat()
    for currency, rate_to_base in rates.items():
        if currency == to_currency:
            exchange_rate = 1.0
        elif base == to_currency:
            exchange_rate = 1 / float(rate_to_base)
        else:
            exchange_rate = float(rate_to_base)
        rows.append({"rate_date": business_date, "from_currency": currency, "to_currency": to_currency, "exchange_rate": round(exchange_rate, 6)})
    return pd.DataFrame(rows)


def fetch_exchange_rates(api_url: str, offline: bool = True, timeout: int = 10) -> pd.DataFrame:
    payload = MOCK_RESPONSE if offline or requests is None else requests.get(api_url, timeout=timeout).json()
    return parse_exchange_rates(payload)


def ingest(api_url: str, pipeline_run_id: str, offline: bool = True) -> pd.DataFrame:
    return add_bronze_metadata(fetch_exchange_rates(api_url, offline=offline), "exchange_rate_api", "rest_json", "exchange_rates_api", pipeline_run_id)
