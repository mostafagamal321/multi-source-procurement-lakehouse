select supplier_id, supplier_name, country, payment_terms, reliability_score, created_at, updated_at from {{ ref('stg_suppliers') }}
