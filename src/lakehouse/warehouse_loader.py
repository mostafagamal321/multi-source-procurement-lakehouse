from __future__ import annotations
from src.utils.db import get_engine
from src.utils.logger import get_logger
LOGGER=get_logger(__name__)
TABLE_MAP={"silver_suppliers":"suppliers","silver_products":"products","silver_purchase_orders":"purchase_orders","silver_invoices":"invoices","silver_shipments":"shipments","silver_inventory":"inventory","silver_exchange_rates":"exchange_rates","silver_warehouse_records":"warehouse_legacy_records"}
def load_silver_to_postgres(datasets, rejected, fail_if_unavailable: bool=False)->None:
    try:
        from sqlalchemy import text
        engine=get_engine()
        with engine.begin() as conn:
            for schema in ['staging','marts','audit']: conn.execute(text(f'create schema if not exists {schema}'))
        for ds,table in TABLE_MAP.items():
            if ds in datasets: datasets[ds].to_sql(table, engine, schema='staging', if_exists='replace', index=False)
        rejected.to_sql('rejected_records', engine, schema='audit', if_exists='replace', index=False)
    except Exception as exc:
        LOGGER.warning('PostgreSQL unavailable; skipped warehouse load: %s', exc)
        if fail_if_unavailable: raise
