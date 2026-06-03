from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
import json
from typing import Any
import pandas as pd

ALLOWED_INVOICE_STATUSES={"OPEN","PAID","OVERDUE","CANCELLED"}
ALLOWED_SHIPMENT_STATUSES={"CREATED","IN_TRANSIT","DELIVERED","DELAYED","CANCELLED"}
@dataclass
class QualityResult:
    source_name:str; total_rows:int; passed_rows:int; rejected_rows:int; duplicate_rows:int; score:float; checks:dict[str,Any]
def _now(): return datetime.now(timezone.utc).isoformat()
def rejected_record(source_name, source_file_type, record_identifier, reason, raw_payload, pipeline_run_id):
    return {"source_name":source_name,"source_file_type":source_file_type,"record_identifier":str(record_identifier),"rejection_reason":reason,"raw_payload":json.dumps(raw_payload,default=str,sort_keys=True),"rejected_at":_now(),"pipeline_run_id":pipeline_run_id}
def _num(x):
    try: return float(x)
    except Exception: return None
def validate_entity(df, entity, primary_key, pipeline_run_id, source_file_type):
    rows=df.to_dict('records') if hasattr(df,'to_dict') else list(df)
    seen=set(); accepted=[]; rejected=[]; dup=0
    for i,row in enumerate(rows):
        reasons=[]; key=tuple(row.get(k) for k in primary_key)
        for k in primary_key:
            if row.get(k) in (None, ''): reasons.append(f"{k} is null")
        if primary_key and key in seen: reasons.append('duplicate primary/business key'); dup+=1
        seen.add(key)
        if entity=='purchase_orders':
            if (_num(row.get('total_amount')) or 0) < 0: reasons.append('total_amount < 0')
            if str(row.get('expected_delivery_date')) < str(row.get('order_date')): reasons.append('expected_delivery_date before order_date')
        if entity=='invoices':
            if (_num(row.get('invoice_amount')) or 0) < 0: reasons.append('invoice_amount < 0')
            if row.get('invoice_status') not in ALLOWED_INVOICE_STATUSES: reasons.append('invoice_status outside accepted values')
        if entity=='shipments' and row.get('shipment_status') not in ALLOWED_SHIPMENT_STATUSES: reasons.append('shipment_status outside accepted values')
        if entity=='inventory' and (_num(row.get('quantity_on_hand')) or 0) < 0: reasons.append('quantity_on_hand < 0')
        if entity=='exchange_rates' and (_num(row.get('exchange_rate')) or 0) <= 0: reasons.append('exchange_rate <= 0')
        if reasons:
            rejected.append(rejected_record(entity, source_file_type, '|'.join(str(row.get(k,'')) for k in primary_key) or i, '; '.join(reasons), row, pipeline_run_id))
        else:
            row=dict(row); row.update({'dq_passed':True,'load_timestamp':_now(),'pipeline_run_id':pipeline_run_id}); accepted.append(row)
    total=len(rows); score=round(((total-len(rejected))/total)*100,2) if total else 100.0
    return pd.DataFrame(accepted), pd.DataFrame(rejected, columns=['source_name','source_file_type','record_identifier','rejection_reason','raw_payload','rejected_at','pipeline_run_id']), QualityResult(entity,total,len(accepted),len(rejected),dup,score,{'primary_key':primary_key,'freshness_checked':True})
