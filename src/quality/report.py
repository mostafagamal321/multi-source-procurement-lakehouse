from __future__ import annotations
import json
from pathlib import Path
from src.quality.checks import QualityResult
from src.utils.config import get_settings

def _counts(rows, key):
    out={}
    for r in rows: out[r.get(key)] = out.get(r.get(key),0)+1
    return out
def render_quality_reports(results:list[QualityResult], rejected)->tuple[Path,Path]:
    settings=get_settings(); rows=rejected.to_dict('records') if hasattr(rejected,'to_dict') else []
    payload={"overall_score":round(sum(r.score for r in results)/len(results),2) if results else 100.0,"sources":[r.__dict__ for r in results],"rejected_records_by_source":_counts(rows,'source_name'),"rejected_records_by_file_type":_counts(rows,'source_file_type')}
    jp=settings.reports_dir/"data_quality_report.json"; mp=settings.reports_dir/"data_quality_report.md"
    jp.write_text(json.dumps(payload,indent=2,default=str),encoding='utf-8')
    lines=["# Data Quality Report","",f"Overall score: **{payload['overall_score']}%**","","| Source | Rows | Passed | Rejected | Duplicates | Score |","|---|---:|---:|---:|---:|---:|"]
    for r in results: lines.append(f"| {r.source_name} | {r.total_rows} | {r.passed_rows} | {r.rejected_rows} | {r.duplicate_rows} | {r.score}% |")
    lines += ["","## Rejected Records by File Type"]+[f"- {k}: {v}" for k,v in payload['rejected_records_by_file_type'].items()]
    mp.write_text('\n'.join(lines)+'\n',encoding='utf-8'); return jp,mp
def render_pipeline_summary(pipeline_run_id:str, bronze_outputs:dict[str,Path], silver_outputs:dict[str,Path])->Path:
    p=get_settings().reports_dir/"pipeline_summary.md"; lines=["# Pipeline Summary","",f"Pipeline run id: `{pipeline_run_id}`","","## Bronze outputs"]+[f"- {n}: `{o}`" for n,o in bronze_outputs.items()]+["","## Silver and rejected outputs"]+[f"- {n}: `{o}`" for n,o in silver_outputs.items()]
    p.write_text('\n'.join(lines)+'\n',encoding='utf-8'); return p
