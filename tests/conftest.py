from __future__ import annotations
import subprocess, sys
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

@pytest.fixture(scope="session", autouse=True)
def sample_sources():
    subprocess.run([sys.executable, str(ROOT / "scripts" / "generate_sample_sources.py")], check=True)
    return ROOT / "sample_data"
