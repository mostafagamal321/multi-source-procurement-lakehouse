select warehouse_id, count(*) as sku_count, sum(low_stock_flag) as low_stock_skus, avg(low_stock_flag) as inventory_risk_rate
from {{ ref('fact_inventory_snapshot') }}
group by 1
