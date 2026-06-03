from __future__ import annotations

import os
import socket
import time


def wait_for_tcp_service(name: str, host: str, port: int, timeout_seconds: int = 120) -> None:
    deadline = time.time() + timeout_seconds

    while time.time() < deadline:
        try:
            with socket.create_connection((host, port), timeout=5):
                print(f"{name} is ready at {host}:{port}")
                return
        except OSError:
            print(f"Waiting for {name} at {host}:{port}...")
            time.sleep(5)

    raise TimeoutError(f"Timed out waiting for {name} on {host}:{port}")


def main() -> None:
    postgres_host = os.getenv("POSTGRES_HOST", "postgres-warehouse")
    postgres_port = int(os.getenv("POSTGRES_PORT", "5432"))

    minio_endpoint = os.getenv("MINIO_ENDPOINT", "minio:9000")
    if ":" in minio_endpoint:
        minio_host, minio_port_raw = minio_endpoint.split(":", 1)
        minio_port = int(minio_port_raw)
    else:
        minio_host = minio_endpoint
        minio_port = 9000

    wait_for_tcp_service("PostgreSQL", postgres_host, postgres_port)
    wait_for_tcp_service("MinIO", minio_host, minio_port)

    print("All required services are ready.")


if __name__ == "__main__":
    main()