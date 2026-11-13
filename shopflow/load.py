"""Transactional PostgreSQL dimension and fact upserts."""
import psycopg


def load_frame(database_url, frame):
    with psycopg.connect(database_url) as conn:
        with conn.cursor() as cur:
            for row in frame.itertuples(index=False):
                day = row.order_date
                date_key = int(day.strftime("%Y%m%d"))
                cur.execute("""INSERT INTO dim_customer(customer_id) VALUES (%s)
                    ON CONFLICT(customer_id) DO NOTHING""", (row.customer_id,))
                cur.execute("""INSERT INTO dim_product(product_id, title, price) VALUES (%s,%s,%s)
                    ON CONFLICT(product_id) DO UPDATE SET title=EXCLUDED.title, price=EXCLUDED.price""",
                    (row.product_id, row.title, row.unit_price))
                cur.execute("""INSERT INTO dim_date(date_key, full_date, year, month, day) VALUES (%s,%s,%s,%s,%s)
                    ON CONFLICT(date_key) DO NOTHING""",
                    (date_key, day, day.year, day.month, day.day))
                cur.execute("SELECT customer_key FROM dim_customer WHERE customer_id=%s", (row.customer_id,))
                customer_key = cur.fetchone()[0]
                cur.execute("SELECT product_key FROM dim_product WHERE product_id=%s", (row.product_id,))
                product_key = cur.fetchone()[0]
                cur.execute("""INSERT INTO fact_order_items
                    (order_id, product_key, customer_key, date_key, quantity, unit_price, line_total)
                    VALUES (%s,%s,%s,%s,%s,%s,%s)
                    ON CONFLICT(order_id,product_key) DO UPDATE SET
                      customer_key=EXCLUDED.customer_key, date_key=EXCLUDED.date_key,
                      quantity=EXCLUDED.quantity, unit_price=EXCLUDED.unit_price,
                      line_total=EXCLUDED.line_total""",
                    (row.order_id, product_key, customer_key, date_key, row.quantity, row.unit_price, row.line_total))
        # psycopg context manager commits on success, rolls back on error.
    return len(frame)


def record_run(database_url, status, extracted, curated, error=None):
    with psycopg.connect(database_url) as conn:
        conn.execute("""INSERT INTO etl_runs(status, extracted_rows, curated_rows, error_message, finished_at)
                        VALUES (%s,%s,%s,%s,NOW())""", (status, extracted, curated, str(error)[:2000] if error else None))
