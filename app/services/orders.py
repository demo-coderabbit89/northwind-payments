"""Order read model."""
import sqlite3

from fastapi import HTTPException

from app.auth import User, require_owner_or_admin
from app.models import Order
from app.services.formatting import to_display_amount


def fetch_order(conn: sqlite3.Connection, order_id: int, user: User) -> Order:
    """Load an order the caller is allowed to see."""
    row = conn.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="not found")
    require_owner_or_admin(user, row["customer_id"])
    return Order(
        id=row["id"],
        customer_id=row["customer_id"],
        amount=to_display_amount(row["amount_cents"]),
        currency=row["currency"],
        card_last4=row["card_last4"],
        status=row["status"],
    )
