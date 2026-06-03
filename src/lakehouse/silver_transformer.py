from __future__ import annotations
import pandas as pd
from src.quality.checks import validate_entity, QualityResult
from src.utils.config import get_settings

METADATA={"source_system","source_file_type","source_file_name","ingestion_timestamp","raw_record_hash","loaded_at"}
def _rows(df): return df.to_dict('records')
def _standardize(rows):
    out=[]
    for row in rows:
        r={k:v for k,v in row.items() if k not in METADATA}
        for k,v in list(r.items()):
            if isinstance(v,str): r[k]=v.strip() or None
            if k in {"currency","from_currency","to_currency","status","invoice_status","shipment_status"} and r[k] is not None: r[k]=str(r[k]).upper()
            if k=="shipment_status" and r[k]=="IN_TRANSIT": r[k]="IN_TRANSIT"
        out.append(r)
    return pd.DataFrame(out)
def transform_datasets(bronze:dict[str,pd.DataFrame], pipeline_run_id:str)->tuple[dict[str,pd.DataFrame],pd.DataFrame,list[QualityResult]]:
    cfg={"purchase_orders":("bronze_purchase_orders",["po_id"],"json"),"shipments":("bronze_shipment_events",["shipment_id","event_timestamp"],"ndjson"),"suppliers":("bronze_suppliers",["supplier_id"],"xml"),"invoices":("bronze_invoices",["invoice_id"],"xlsx"),"inventory":("bronze_inventory",["snapshot_date","warehouse_id","product_id"],"parquet"),"products":("bronze_product_catalog",["product_id"],"avro"),"warehouse_records":("bronze_warehouse_legacy_records",["warehouse_id","product_id"],"fixed_width_txt"),"exchange_rates":("bronze_exchange_rates",["rate_date","from_currency","to_currency"],"rest_json")}
    silver={}; rejects=[]; results=[]
    for entity,(b,pk,ft) in cfg.items():
        acc,rej,res=validate_entity(_standardize(_rows(bronze[b])),entity,pk,pipeline_run_id,ft)
        silver[f"silver_{entity}"]=acc; rejects.append(rej); results.append(res)
    return silver, pd.concat(rejects, ignore_index=True), results
def write_silver_dataset(df, dataset_name, pipeline_run_id):
    target=get_settings().lakehouse_dir/"silver"/dataset_name/f"pipeline_run_id={pipeline_run_id}"; target.mkdir(parents=True,exist_ok=True)
    output=target/"part-00000.parquet"; df.to_parquet(output,index=False); return output
def write_silver_many(datasets,rejected,pipeline_run_id):
    outputs={n:write_silver_dataset(d,n,pipeline_run_id) for n,d in datasets.items()}
    target=get_settings().lakehouse_dir/"rejected"/"rejected_records"/f"pipeline_run_id={pipeline_run_id}"; target.mkdir(parents=True,exist_ok=True)
    rejected.to_parquet(target/"part-00000.parquet",index=False); outputs["rejected_records"]=target/"part-00000.parquet"; return outputs
