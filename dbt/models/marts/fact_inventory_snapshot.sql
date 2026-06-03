select snapshot_date::date, warehouse_id, product_id, quantity_on_hand::numeric, reorder_level::numeric,
       case when quantity_on_hand::numeric < reorder_level::numeric then 1 else 0 end as low_stock_flag
from {{ ref('stg_inventory') }}
