from datetime import date
from decimal import Decimal
from shopflow.transform import transform_carts


def test_cleaning_and_revenue():
    carts = [{"id": 10, "userId": 5, "products": [
        {"id": 3, "title": "  Keyboard  ", "quantity": 2, "price": 19.995},
        {"id": 4, "title": "", "quantity": 1, "price": 3},
        {"id": 5, "title": "Mouse", "quantity": -2, "price": 9},
    ]}]
    result = transform_carts(carts, date(2026, 11, 13))
    assert len(result) == 1
    assert result.iloc[0]["title"] == "Keyboard"
    assert result.iloc[0]["unit_price"] == Decimal("20.00")
    assert result.iloc[0]["line_total"] == Decimal("40.00")


def test_deduplicates_fact_grain():
    item = {"id": 7, "title": "Book", "quantity": 1, "price": 12}
    result = transform_carts([{"id": 1, "userId": 2, "products": [item, item]}])
    assert len(result) == 1


def test_empty_input():
    assert transform_carts([]).empty
