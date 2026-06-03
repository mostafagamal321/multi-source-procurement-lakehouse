create schema if not exists staging;
create schema if not exists marts;
create schema if not exists audit;
create schema if not exists snapshots;

create table if not exists audit.rejected_records (
  source_name text,
  source_file_type text,
  record_identifier text,
  rejection_reason text,
  raw_payload text,
  rejected_at timestamptz,
  pipeline_run_id text
);
