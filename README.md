# ShopFlow | E-Commerce ETL Pipeline

**Python • Pandas • PostgreSQL • REST APIs • Docker • SQL**

## Project Overview

ShopFlow is a Python-based ETL (Extract, Transform, Load) pipeline designed to automate the ingestion, cleaning, transformation, and storage of e-commerce data.

The pipeline extracts JSON records from REST APIs, processes them using Pandas, and loads structured data into PostgreSQL using a dimensional Star Schema.

## Architecture

```text
E-Commerce REST API (DummyJSON)
           |
           v
    EXTRACT (Requests)
    - API pagination
    - HTTP status validation
    - Retry logic
    - Exception handling
           |
           v
    TRANSFORM (Pandas)
    - Missing-value handling
    - Data type standardization
    - Duplicate removal
    - Data validation
           |
           v
    LOAD (PostgreSQL)
    - Fact table
    - Dimension tables
    - Transactional upserts
           |
           v
    SQL ANALYTICS
    - Sales analysis
    - Product performance
    - Customer spending
```

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | ETL pipeline development |
| Requests | REST API integration |
| Pandas | Data cleaning and transformation |
| PostgreSQL | Relational database |
| SQL | Data modeling and analytics |
| Docker | Database environment |
| Pytest | Automated testing |

## Key Features

- Automated extraction of paginated JSON data from REST APIs.
- HTTP status-code validation, exception handling, and retry mechanisms.
- Data cleaning, missing-value handling, and type standardization.
- Duplicate detection and removal.
- PostgreSQL Star Schema with fact and dimension tables.
- Transactional database loading with idempotent upserts.
- ETL execution auditing.
- SQL queries for analytical reporting.

## Database Design

**Fact Table**

`fact_order_items`

Stores order-product records, quantities, unit prices, and line totals.

**Dimension Tables**

- `dim_customer`: Customer identifiers.
- `dim_product`: Product information and observed prices.
- `dim_date`: ETL snapshot dates.

**Audit Table**

`etl_runs`: Tracks pipeline execution outcomes and errors.

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/ShopFlow.git
cd ShopFlow
```

Replace `YOUR_USERNAME` with your GitHub username after publishing the repository.

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy `.env.example` to `.env`.

### 5. Start PostgreSQL

```bash
docker compose up -d
```

### 6. Execute the ETL Pipeline

```bash
python -m shopflow.main
```

### 7. Run Automated Tests

```bash
pytest -q
```

## Data Quality and Reliability

ShopFlow validates incoming records before loading them into PostgreSQL.

Invalid records, including missing identifiers, negative prices, and nonpositive quantities, are excluded.

Database transactions help prevent partial data loads, while upserts support repeatable execution without duplicating existing order-product records.

## Analytical Use Cases

The curated data supports:

1. Product sales performance analysis.
2. Customer spending analysis.
3. Total revenue calculations.
4. Order quantity analysis.

**Note:** DummyJSON provides sample cart data rather than real transactions. The date dimension represents the ETL snapshot date, not the original purchase date.

## Testing

The project includes automated tests for API extraction and data transformation.

A successful local run should be verified using pipeline logs, PostgreSQL records, and SQL query outputs.

## Future Enhancements

- Apache Airflow orchestration.
- Incremental data extraction.
- Cloud database deployment.
- Structured monitoring and alerts.
- Power BI or Streamlit dashboards.
- CI/CD using GitHub Actions.

## Author

**ShopFlow | Data Engineering Portfolio Project**

Built to demonstrate Python ETL development, REST API integration, data transformation, relational data modeling, and SQL analytics.

## License

Add a license file before public distribution.
