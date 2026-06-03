from __future__ import annotations
from src.utils.config import Settings, get_settings

def warehouse_url(settings: Settings | None = None) -> str:
    s=settings or get_settings(); return f"postgresql+psycopg2://{s.warehouse_user}:{s.warehouse_password}@{s.warehouse_host}:{s.warehouse_port}/{s.warehouse_db}"
def get_engine(settings: Settings | None = None):
    from sqlalchemy import create_engine
    return create_engine(warehouse_url(settings), pool_pre_ping=True)
