select source_name, rejection_reason, count(*) as records from audit.rejected_records group by 1,2
