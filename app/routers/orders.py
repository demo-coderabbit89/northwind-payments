from fastapi import APIRouter, Depends, HTTPException

from app import db
from app.auth import User, current_user, require_owner_or_admin
from app.models import CaptureRequest, Order
from app.services import payments

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("", response_model=Order, status_code=201)
def create_order(req: CaptureRequest, user: User = Depends(current_user)) -> Order:
    require_owner_or_admin(user, req.customer_id)
    with db.transaction() as conn:
        order_id = payments.capture(conn, user.id, req)
    return get_order(order_id, user)


@router.get("/{order_id}", response_model=Order)
def get_order(order_id: int, user: User = Depends(current_user)) -> Order:
    row = db.get_conn().execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="not found")
    require_owner_or_admin(user, row["customer_id"])
    return Order(**dict(row))
