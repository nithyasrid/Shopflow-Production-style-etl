# ShopFlow: E-Commerce REST API to PostgreSQL ETL

An executable Python/Pandas/PostgreSQL ETL portfolio project with REST ingestion, resilient HTTP retries, data validation, a dimensional star schema, idempotent upserts, run auditing, and analytical SQL.

## Architecture

```text
DummyJSON /carts REST API
    |  GET /carts?limit=20&skip=0 ... (pagination, timeout, retries)
    v
Extract (requests) -> Transform (pandas + Decimal) -> Load (psycopg transaction)
                                                        |
                                                        v
                                       PostgreSQL star schema
                                 dim_customer   dim_product   dim_date
                                            \      |      /
                                            fact_order_items
                                                        |
                                                        v
                                              SQL analytics queries
```

## Run locally

Prerequisites: Python 3.10+, Docker with Docker Compose, internet connection.

```bash
cp .env.example .env
# Windows PowerShell: Copy-Item .env.example .env
python -m venv .venv
# macOS/Linux: source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
docker compose up -d
python -m shopflow.main
# Optional reproducible snapshot date:
python -m shopflow.main --date 2026-11-13
pytest -q
```

Query results:

```bash
docker compose exec -T postgres psql -U shopflow -d shopflow < sql/analytics.sql
```

Windows PowerShell alternative:

```powershell
Get-Content sql/analytics.sql | docker compose exec -T postgres psql -U shopflow -d shopflow
```

## Star schema

- `fact_order_items`: grain = **one order ID + product ID**. Measures: quantity, unit price, line total. Surrogate dimension foreign keys.
- `dim_customer`: API user identifier.
- `dim_product`: API product identifier, title, latest observed unit price.
- `dim_date`: **ETL snapshot date**, not order date. DummyJSON carts do not supply purchase timestamps.
- `etl_runs`: execution audit rows and error details.

## Data quality and operational behavior

- Retries GET requests for 429 and transient 5xx responses with backoff; checks HTTP errors, response structure, and pagination.
- Drops invalid item lines (missing IDs, invalid/negative price, nonpositive quantity, blank title); rounds monetary amounts with `Decimal`.
- Deduplicates on `(order_id, product_id)`; SQL upserts make repeated loads idempotent for the same cart data.
- Database load runs inside a transaction; failures roll back data changes. A separate audit insert records run outcome when the database is reachable.
- A product's latest observed title and price replace older dimension values. The fact preserves its own loaded unit price.

## Known limitations / next steps

This is a **portfolio-ready baseline**, not a deployed production service. The DummyJSON API is sample data, not live sales. There is no authentic purchase date, order status, customer profile, historical product SCD, or incremental change feed. Snapshot date is only the ingestion date, so avoid interpreting the date report as historical daily sales. Full refresh reads all carts; production extensions would include orchestration, secrets management, structured monitoring, integration tests with ephemeral Postgres, incremental extraction, and a data warehouse deployment.

## Suggested resume description (after running and verifying)

Built a Python ETL pipeline that paginates e-commerce REST JSON, retries transient HTTP failures, validates and normalizes line items using Pandas, and transactionally upserts a PostgreSQL star schema with analytical queries and run audits.
