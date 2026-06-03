select shipment_id, po_id, warehouse_id, shipment_status, event_timestamp::timestamp, carrier, delay_reason,
       case when shipment_status = 'DELAYED' then 1 else 0 end as delayed_flag
from {{ ref('stg_shipments') }}
