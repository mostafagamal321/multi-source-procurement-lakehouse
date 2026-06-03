select po.supplier_id, s.supplier_name, fs.carrier, count(*) as shipment_events,
       sum(fs.delayed_flag) as delayed_shipments, avg(fs.delayed_flag) as delay_rate
from {{ ref('fact_shipments') }} fs
left join {{ ref('fact_purchase_orders') }} po using (po_id)
left join {{ ref('dim_supplier') }} s on s.supplier_id = po.supplier_id
group by 1,2,3
