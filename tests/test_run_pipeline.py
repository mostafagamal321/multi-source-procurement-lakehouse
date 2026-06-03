from pathlib import Path
import subprocess, sys


def test_local_pipeline_generates_reports():
    root = Path(__file__).resolve().parents[1]
    subprocess.run([sys.executable, str(root / "scripts" / "run_local_pipeline.py")], cwd=root, check=True)
    assert (root / "reports" / "data_quality_report.json").exists()
    assert (root / "reports" / "pipeline_summary.md").exists()
