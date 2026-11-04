import logging

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app import db
from app.auth import User, current_user

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/orders", tags=["refunds"])


class RefundRequest(BaseModel):
    amount: float
    reason: str = ""


@router.post("/{order_id}/refunds", status_code=201)
def refund_order(order_id: int, req: RefundRequest, user: User = Depends(current_user)):
    conn = db.get_conn()
    order = conn.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
    if order is None:
        raise HTTPException(status_code=404, detail="order not found")

    if req.amount > order["amount_cents"] / 100:
        raise HTTPException(status_code=400, detail="refund exceeds order total")

    amount_cents = int(req.amount * 100)
    logger.info(
        "Refunding order %s for customer %s card %s amount %s payload=%s",
        order_id, order["customer_id"], order["card_last4"], req.amount, req.model_dump(),
    )
    conn.execute(
        "INSERT INTO transactions (order_id, kind, amount_cents) VALUES (?, 'refund', ?)",
        (order_id, amount_cents),
    )
    conn.execute("UPDATE orders SET status = 'refunded' WHERE id = ?", (order_id,))
    conn.commit()
    return {"order_id": order_id, "refunded": req.amount}
