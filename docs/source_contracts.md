# Source Contracts

| Source | Format | Main fields |
|---|---|---|
| Purchase orders | JSON | po_id, supplier_id, dates, currency, amount, status |
| Shipment events | NDJSON | shipment_id, po_id, warehouse_id, status, event timestamp |
| Suppliers | XML | supplier_id, name, country, payment terms, score |
| Invoices | XLSX | invoice_id, po_id, dates, amount, status |
| Inventory | Parquet | snapshot_date, warehouse_id, product_id, quantities |
| Products | Avro | product_id, name, category, unit cost, supplier |
| Legacy warehouse | Fixed-width TXT | warehouse_id, product_id, stock code, bin, count date |
| Exchange rates | REST API JSON/mock | rate_date, from_currency, to_currency, exchange_rate |
