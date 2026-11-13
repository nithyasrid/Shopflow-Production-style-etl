CREATE TABLE IF NOT EXISTS dim_customer (
    customer_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_id BIGINT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS dim_product (
    product_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    product_id BIGINT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    price NUMERIC(12,2) NOT NULL CHECK (price >= 0)
);
CREATE TABLE IF NOT EXISTS dim_date (
    date_key INTEGER PRIMARY KEY,
    full_date DATE NOT NULL UNIQUE,
    year INTEGER NOT NULL,
    month INTEGER NOT NULL,
    day INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS fact_order_items (
    order_id BIGINT NOT NULL,
    product_key BIGINT NOT NULL REFERENCES dim_product(product_key),
    customer_key BIGINT NOT NULL REFERENCES dim_customer(customer_key),
    date_key INTEGER NOT NULL REFERENCES dim_date(date_key),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(12,2) NOT NULL CHECK (unit_price >= 0),
    line_total NUMERIC(14,2) NOT NULL CHECK (line_total >= 0),
    PRIMARY KEY (order_id, product_key)
);
CREATE INDEX IF NOT EXISTS ix_fact_customer ON fact_order_items(customer_key);
CREATE INDEX IF NOT EXISTS ix_fact_date ON fact_order_items(date_key);
CREATE TABLE IF NOT EXISTS etl_runs (
    run_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    finished_at TIMESTAMPTZ,
    status TEXT NOT NULL,
    extracted_rows INTEGER NOT NULL DEFAULT 0,
    curated_rows INTEGER NOT NULL DEFAULT 0,
    error_message TEXT
);
