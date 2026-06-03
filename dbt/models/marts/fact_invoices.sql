{{ config(materialized='table', schema='marts') }}

select
    invoice_id,
    po_id,
    supplier_id,
    invoice_date::date as invoice_date,
    due_date::date as due_date,
    nullif(paid_date, '')::date as paid_date,
    invoice_amount::numeric as invoice_amount,
    currency,
    invoice_status,

    (
        coalesce(nullif(paid_date, '')::date, current_date)
        - due_date::date
    )::int as payment_delay_days,

    case
        when coalesce(nullif(paid_date, '')::date, current_date) > due_date::date then true
        else false
    end as is_late,

    current_timestamp as loaded_at

from {{ ref('stg_invoices') }}