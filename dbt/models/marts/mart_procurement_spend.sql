{{ config(materialized='table', schema='marts') }}

with purchase_orders as (
    select
        po_id,
        supplier_id,
        order_date::date as order_date,
        currency,
        total_amount::numeric as total_amount,
        status
    from {{ ref('fact_purchase_orders') }}
),

exchange_rates as (
    select
        rate_date::date as rate_date,
        from_currency,
        to_currency,
        nullif(exchange_rate, '')::numeric as exchange_rate
    from {{ ref('stg_exchange_rates') }}
),

suppliers as (
    select
        supplier_id,
        supplier_name,
        country
    from {{ ref('dim_supplier') }}
)

select
    date_trunc('month', po.order_date)::date as spend_month,
    po.supplier_id,
    s.supplier_name,
    s.country,
    po.currency,

    count(distinct po.po_id) as purchase_order_count,
    sum(po.total_amount) as spend_original_currency,

    sum(
        po.total_amount * coalesce(er.exchange_rate, 1::numeric)
    ) as spend_egp,

    current_timestamp as loaded_at

from purchase_orders po

left join suppliers s
    on po.supplier_id = s.supplier_id

left join exchange_rates er
    on po.currency = er.from_currency
    and er.to_currency = 'EGP'
    and po.order_date = er.rate_date

group by
    date_trunc('month', po.order_date)::date,
    po.supplier_id,
    s.supplier_name,
    s.country,
    po.currency