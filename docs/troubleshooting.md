# Troubleshooting

- If Superset cannot connect, use host `postgres-warehouse`, port `5432`, database `procurement` inside Docker.
- If local Python lacks dependencies, run `python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt`.
- If public exchange API fails, keep `OFFLINE_API_MODE=true`.
- If ports conflict, stop local services using ports 8080, 8081, 8088, 9000, 9001, or 5434.
