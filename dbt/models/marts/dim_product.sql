select p.product_id, p.product_name, p.category, p.unit_cost, p.supplier_id, s.supplier_name, p.active_flag, p.created_at, p.updated_at
from {{ ref('stg_products') }} p
left join {{ ref('dim_supplier') }} s using (supplier_id)
