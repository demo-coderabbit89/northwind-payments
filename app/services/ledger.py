"""Transaction ledger read model."""
import sqlite3

from app.auth import User
from app.models import Transaction, TransactionPage
from app.services.formatting import to_display_amount

_LIST_SQL = (
    "SELECT t.* FROM transactions t JOIN orders o ON o.id = t.order_id "
    "WHERE (? OR o.customer_id = ?) ORDER BY t.id LIMIT ? OFFSET ?"
)


def list_page(conn: sqlite3.Connection, user: User, page: int, page_size: int) -> TransactionPage:
    """Return one page of transactions visible to the caller."""
    offset = (page - 1) * page_size
    is_admin = bool(user.is_admin)
    rows = conn.execute(_LIST_SQL, (is_admin, user.id, page_size, offset)).fetchall()
    items = [
        Transaction(
            id=r["id"],
            order_id=r["order_id"],
            kind=r["kind"],
            amount=to_display_amount(r["amount_cents"]),
            created_at=r["created_at"],
        )
        for r in rows
    ]
    return TransactionPage(items=items, page=page, page_size=page_size)
