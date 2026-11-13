"""CLI entry point: python -m shopflow.main."""
import argparse
import logging
import os
from datetime import date
from dotenv import load_dotenv
from .extract import extract_carts
from .transform import transform_carts
from .load import load_frame, record_run


def main():
    load_dotenv()
    parser = argparse.ArgumentParser(description="ShopFlow REST-to-Postgres ETL")
    parser.add_argument("--date", help="Snapshot date in YYYY-MM-DD format (default: today)")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    database_url = os.environ["DATABASE_URL"]
    snapshot_date = date.fromisoformat(args.date) if args.date else date.today()
    extracted = curated = 0
    try:
        carts = extract_carts(os.getenv("API_URL", "https://dummyjson.com/carts"),
                              page_size=int(os.getenv("PAGE_SIZE", "20")),
                              timeout=int(os.getenv("API_TIMEOUT", "20")),
                              retries=int(os.getenv("API_RETRIES", "3")))
        extracted = len(carts)
        frame = transform_carts(carts, snapshot_date)
        curated = len(frame)
        loaded = load_frame(database_url, frame)
        record_run(database_url, "success", extracted, curated)
        logging.info("ETL completed: %s carts, %s curated lines, %s loaded lines", extracted, curated, loaded)
    except Exception as exc:
        logging.exception("ETL failed")
        try:
            record_run(database_url, "failed", extracted, curated, exc)
        except Exception:
            logging.exception("Unable to persist failed run audit")
        raise


if __name__ == "__main__":
    main()
