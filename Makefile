build:
	docker compose build
up:
	docker compose up -d
down:
	docker compose down
restart:
	docker compose restart
logs:
	docker compose logs -f
test:
	PYTHONPATH=. pytest -q
lint:
	ruff check .
generate-sources:
	PYTHONPATH=. python scripts/generate_sample_sources.py
upload-sources:
	PYTHONPATH=. python scripts/upload_sources_to_minio.py
run-pipeline:
	PYTHONPATH=. python scripts/run_local_pipeline.py
quality:
	PYTHONPATH=. python scripts/run_quality_checks.py
dbt-build:
	cd dbt && dbt build --profiles-dir .
reset:
	docker compose down -v && rm -rf .lakehouse reports/data_quality_report.* reports/pipeline_summary.md
