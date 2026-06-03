"""Configuration helpers for the procurement lakehouse platform."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os

PROJECT_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Settings:
    project_root: Path = PROJECT_ROOT
    sample_data_dir: Path = PROJECT_ROOT / "sample_data"
    lakehouse_dir: Path = PROJECT_ROOT / ".lakehouse"
    reports_dir: Path = PROJECT_ROOT / "reports"
    minio_endpoint: str = os.getenv("MINIO_ENDPOINT", "localhost:9000")
    minio_access_key: str = os.getenv("MINIO_ROOT_USER", "minioadmin")
    minio_secret_key: str = os.getenv("MINIO_ROOT_PASSWORD", "minioadmin")
    minio_secure: bool = os.getenv("MINIO_SECURE", "false").lower() == "true"
    warehouse_host: str = os.getenv("POSTGRES_HOST", "localhost")
    warehouse_port: int = int(os.getenv("POSTGRES_PORT", "5434"))
    warehouse_db: str = os.getenv("POSTGRES_DB", "procurement")
    warehouse_user: str = os.getenv("POSTGRES_USER", "procurement")
    warehouse_password: str = os.getenv("POSTGRES_PASSWORD", "procurement")
    exchange_api_url: str = os.getenv("EXCHANGE_API_URL", "https://open.er-api.com/v6/latest/USD")
    offline_api_mode: bool = os.getenv("OFFLINE_API_MODE", "true").lower() == "true"

    @property
    def buckets(self) -> tuple[str, ...]:
        return ("landing", "bronze", "silver", "rejected", "reports")


def get_settings() -> Settings:
    """Return runtime settings sourced from environment variables."""
    settings = Settings()
    settings.lakehouse_dir.mkdir(parents=True, exist_ok=True)
    settings.reports_dir.mkdir(parents=True, exist_ok=True)
    return settings
