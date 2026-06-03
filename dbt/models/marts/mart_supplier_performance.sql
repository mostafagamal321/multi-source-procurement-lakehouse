select s.supplier_id, s.supplier_name, count(distinct po.po_id) as purchase_order_count,
       sum(po.total_amount) as total_spend_native,
       avg(i.payment_delay_days) as avg_invoice_delay_days,
       avg(fs.delayed_flag) as shipment_delay_rate
from {{ ref('dim_supplier') }} s
left join {{ ref('fact_purchase_orders') }} po on po.supplier_id = s.supplier_id
left join {{ ref('fact_invoices') }} i on i.supplier_id = s.supplier_id
left join {{ ref('fact_shipments') }} fs on fs.po_id = po.po_id
group by 1,2
