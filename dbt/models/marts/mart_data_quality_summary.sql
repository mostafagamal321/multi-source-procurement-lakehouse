select source_name, source_file_type, count(*) as rejected_records
from audit.rejected_records
group by 1,2
