from pathlib import Path
import os
from minio import Minio

PROJECT_ROOT = Path("/opt/app")

client = Minio(
    os.getenv("MINIO_ENDPOINT", "minio:9000"),
    access_key=os.getenv("MINIO_ROOT_USER", "minioadmin"),
    secret_key=os.getenv("MINIO_ROOT_PASSWORD", "minioadmin"),
    secure=False,
)

bucket_paths = {
    "bronze": PROJECT_ROOT / ".lakehouse" / "bronze",
    "silver": PROJECT_ROOT / ".lakehouse" / "silver",
    "rejected": PROJECT_ROOT / ".lakehouse" / "rejected",
    "reports": PROJECT_ROOT / "reports",
}

for bucket, folder in bucket_paths.items():
    if not client.bucket_exists(bucket):
        client.make_bucket(bucket)

    if not folder.exists():
        print(f"Skipping missing folder: {folder}")
        continue

    for file_path in folder.rglob("*"):
        if file_path.is_file():
            object_name = file_path.relative_to(folder).as_posix()
            client.fput_object(bucket, object_name, str(file_path))
            print(f"Uploaded {file_path} -> {bucket}/{object_name}")

print("MinIO output upload completed.")