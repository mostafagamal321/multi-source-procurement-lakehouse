-- Total procurement spend
select sum(spend_usd) as total_procurement_spend_usd from marts.mart_procurement_spend;
-- Spend by supplier
select supplier_name, sum(spend_usd) as spend_usd from marts.mart_procurement_spend group by 1 order by 2 desc;
-- Spend by product category
select category, sum(spend_usd) as spend_usd from marts.mart_procurement_spend group by 1 order by 2 desc;
-- Monthly procurement trend
select order_month, sum(spend_usd) as spend_usd from marts.mart_procurement_spend group by 1 order by 1;
-- Invoice payment delay
select supplier_id, avg(payment_delay_days) as avg_payment_delay_days from marts.fact_invoices group by 1 order by 2 desc;
-- Shipment delay rate
select carrier, avg(delayed_flag) as delay_rate from marts.fact_shipments group by 1 order by 2 desc;
-- Inventory risk by warehouse
select warehouse_id, low_stock_skus, inventory_risk_rate from marts.mart_inventory_risk order by inventory_risk_rate desc;
-- Top delayed suppliers
select supplier_name, shipment_delay_rate from marts.mart_supplier_performance order by shipment_delay_rate desc nulls last;
-- Data quality score by source (use JSON report for score; rejected table for operational count)
select source_name, source_file_type, rejected_records from marts.mart_data_quality_summary order by rejected_records desc;
-- Rejected records by file type
select source_file_type, count(*) as rejected_records from audit.rejected_records group by 1 order by 2 desc;
-- Exchange-rate-adjusted procurement cost
select supplier_name, currency, sum(spend_native) as spend_native, sum(spend_usd) as spend_usd from marts.mart_procurement_spend group by 1,2 order by 4 desc;
