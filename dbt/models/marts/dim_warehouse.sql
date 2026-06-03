select distinct warehouse_id from {{ ref('stg_inventory') }}
union
select distinct warehouse_id from {{ ref('stg_shipments') }}
