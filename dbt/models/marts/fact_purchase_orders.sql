{{ config(materialized='table', schema='marts') }}

select
    po_id,
    supplier_id,
    order_date::date as order_date,
    expected_delivery_date::date as expected_delivery_date,
    currency,
    total_amount::numeric as total_amount,
    status,

    (
        expected_delivery_date::date
        - order_date::date
    )::int as expected_delivery_days,

    'manual_load' as pipeline_run_id,
    current_timestamp as loaded_at

from {{ ref('stg_purchase_orders') }}