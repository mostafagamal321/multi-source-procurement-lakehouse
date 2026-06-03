from __future__ import annotations
from pathlib import Path
from src.utils.config import get_settings

def get_minio_client():
    from minio import Minio
    s=get_settings(); return Minio(s.minio_endpoint, access_key=s.minio_access_key, secret_key=s.minio_secret_key, secure=s.minio_secure)
def ensure_buckets():
    c=get_minio_client()
    for b in get_settings().buckets:
        if not c.bucket_exists(b): c.make_bucket(b)
def upload_file(bucket:str, object_name:str, path:str|Path): get_minio_client().fput_object(bucket, object_name, str(path))
