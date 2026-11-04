"""Payment business logic."""
import sqlite3

from app import audit
from app.services import webhooks
from app.models import CaptureRequest


def capture(conn: sqlite3.Connection, actor_id: int, req: CaptureRequest) -> int:
    cur = conn.execute(
        "INSERT INTO orders (customer_id, amount_cents, currency, card_last4) VALUES (?, ?, ?, ?)",
        (req.customer_id, req.amount_cents, req.currency, req.card_last4),
    )
    order_id = cur.lastrowid
    conn.execute(
        "INSERT INTO transactions (order_id, kind, amount_cents) VALUES (?, 'capture', ?)",
        (order_id, req.amount_cents),
    )
    audit.record(conn, actor_id, "capture", "order", order_id, {"amount_cents": req.amount_cents})
    webhooks.notify("payment.captured", {"order_id": order_id, "amount_cents": req.amount_cents})
    return order_id
