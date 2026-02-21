ALTER USER metadata WITH SUPERUSER;

CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- =====================
-- DATASETS
-- =====================
CREATE TABLE datasets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    uri TEXT UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================
-- COLUMNS (SCHEMA)
-- =====================
CREATE TABLE columns (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    dataset_id UUID REFERENCES datasets(id) ON DELETE CASCADE,
    column_name VARCHAR(255),
    data_type VARCHAR(100),
    is_nullable BOOLEAN DEFAULT TRUE
);

-- =====================
-- JOBS
-- =====================
CREATE TABLE jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    job_name VARCHAR(255) UNIQUE,
    description TEXT
);

-- =====================
-- RUNS
-- =====================
CREATE TABLE runs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    job_id UUID REFERENCES jobs(id),
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    status VARCHAR(50)
);

-- =====================
-- COLUMN STATISTICS
-- =====================
CREATE TABLE column_statistics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    column_id UUID REFERENCES columns(id),
    run_id UUID REFERENCES runs(id),
    null_fraction FLOAT,
    distinct_count INTEGER,
    min_value TEXT,
    max_value TEXT
);

-- =====================
-- DATA QUALITY RESULTS
-- =====================
CREATE TABLE data_quality_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    run_id UUID REFERENCES runs(id) ON DELETE CASCADE,
    dataset_id UUID REFERENCES datasets(id) ON DELETE CASCADE,
    check_name VARCHAR(255) NOT NULL,
    success BOOLEAN,
    observed_value VARCHAR(255),
    expected_value VARCHAR(255),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================
-- LINEAGE GRAPH
-- =====================
CREATE TABLE lineage_edges (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_dataset_id UUID REFERENCES datasets(id) ON DELETE CASCADE,
    target_dataset_id UUID REFERENCES datasets(id) ON DELETE CASCADE,
    job_run_id UUID REFERENCES runs(id) ON DELETE CASCADE,
    edge_type VARCHAR(50)
);