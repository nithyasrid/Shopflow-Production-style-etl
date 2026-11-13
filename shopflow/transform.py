"""Validate and normalize cart product lines into a fact-ready DataFrame."""
from datetime import date
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import logging
import pandas as pd

LOG = logging.getLogger(__name__)
COLUMNS = ["order_id", "customer_id", "product_id", "title", "quantity", "unit_price", "line_total", "order_date"]


def money(value):
    try:
        amount = Decimal(str(value))
        if not amount.is_finite() or amount < 0:
            return None
        return amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    except (InvalidOperation, ValueError, TypeError):
        return None


def positive_int(value):
    if isinstance(value, bool):
        return None
    try:
        number = int(value)
        return number if number > 0 and str(value).strip() == str(number) else None
    except (ValueError, TypeError):
        return None


def transform_carts(carts, snapshot_date=None):
    """DummyJSON carts have no order date; use the ETL snapshot date, not a claimed purchase date."""
    snapshot_date = snapshot_date or date.today()
    rows = []
    rejected = 0
    for cart in carts:
        order_id = positive_int(cart.get("id")) if isinstance(cart, dict) else None
        customer_id = positive_int(cart.get("userId")) if isinstance(cart, dict) else None
        products = cart.get("products", []) if isinstance(cart, dict) else []
        if not isinstance(products, list):
            products = []
        for item in products:
            if not isinstance(item, dict):
                rejected += 1
                continue
            product_id = positive_int(item.get("id"))
            quantity = positive_int(item.get("quantity"))
            price = money(item.get("price"))
            title = str(item.get("title") or "").strip()
            if None in (order_id, customer_id, product_id, quantity, price) or not title:
                rejected += 1
                continue
            rows.append({"order_id": order_id, "customer_id": customer_id,
                         "product_id": product_id, "title": title, "quantity": quantity,
                         "unit_price": price, "line_total": (price * quantity).quantize(Decimal("0.01")),
                         "order_date": snapshot_date})
    frame = pd.DataFrame(rows, columns=COLUMNS)
    if not frame.empty:
        # One order/product pair is the declared fact grain.
        frame = frame.drop_duplicates(subset=["order_id", "product_id"], keep="last").reset_index(drop=True)
    LOG.info("Curated %s order lines; rejected %s invalid lines", len(frame), rejected)
    return frame
