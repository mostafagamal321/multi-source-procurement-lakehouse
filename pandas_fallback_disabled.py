"""Tiny pandas fallback for offline CI environments; Docker uses real pandas."""
from __future__ import annotations
import json
from pathlib import Path

class Series(list):
    def tolist(self): return list(self)
    def nunique(self): return len(set(self))
    def all(self): return all(self)
    def __gt__(self, other): return Series([x > other for x in self])

class _Loc:
    def __init__(self, df): self.df=df
    def __getitem__(self, key):
        r,c=key
        return self.df.rows[r].get(c)

class DataFrame:
    def __init__(self, data=None, columns=None):
        self.rows=list(data or [])
        if columns:
            self.columns=list(columns)
        else:
            seen=[]
            for row in self.rows:
                for k in row:
                    if k not in seen: seen.append(k)
            self.columns=seen
        self.loc=_Loc(self)
    def __len__(self): return len(self.rows)
    def __getitem__(self, key): return Series([r.get(key) for r in self.rows])
    def copy(self): return DataFrame([dict(r) for r in self.rows], self.columns)
    def to_dict(self, orient='records'):
        return [dict(r) for r in self.rows]
    def insert(self, idx, col, value):
        vals = value if isinstance(value, list) else [value]*len(self.rows)
        for r,v in zip(self.rows, vals): r[col]=v
        if col not in self.columns: self.columns.insert(idx,col)
    def to_parquet(self, path, index=False): Path(path).write_text(json.dumps(self.rows, default=str), encoding='utf-8')
    def to_excel(self, writer, sheet_name='Sheet1', index=False): Path(writer.path).write_text(json.dumps(self.rows, default=str), encoding='utf-8')
    def to_sql(self, *a, **k): return None

class ExcelWriter:
    def __init__(self, path, engine=None): self.path=path
    def __enter__(self): return self
    def __exit__(self,*a): return False

def read_excel(path, sheet_name=None): return DataFrame(json.loads(Path(path).read_text(encoding='utf-8')))
def read_parquet(path): return DataFrame(json.loads(Path(path).read_text(encoding='utf-8')))
def read_fwf(path, widths, names, dtype=str):
    rows=[]
    for line in Path(path).read_text(encoding='utf-8').splitlines():
        pos=0; row={}
        for name,width in zip(names,widths):
            row[name]=line[pos:pos+width].strip(); pos+=width
        rows.append(row)
    return DataFrame(rows)
def concat(frames, ignore_index=True):
    rows=[]
    for f in frames: rows.extend(f.to_dict('records'))
    return DataFrame(rows)
def to_numeric(v, errors='coerce'):
    try: return float(v)
    except Exception: return None
