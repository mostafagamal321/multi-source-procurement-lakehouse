{% snapshot supplier_snapshot %}
{{ config(target_schema='snapshots', unique_key='supplier_id', strategy='timestamp', updated_at='updated_at') }}
select * from {{ ref('stg_suppliers') }}
{% endsnapshot %}
