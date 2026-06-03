from __future__ import annotations
import json

def parse_schema(schema): return schema

def writer(fh, schema, records):
    fh.write(json.dumps(records).encode())

def reader(fh):
    return iter(json.loads(fh.read().decode()))
