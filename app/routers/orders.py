from fastapi import APIRouter, Depends

from app import db
from app.auth import User, current_user, require_owner_or_admin
from app.models import CaptureRequest, Order
from app.services import orders as order_service
from app.services import payments

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("", response_model=Order, status_code=201)
def create_order(req: CaptureRequest, user: User = Depends(current_user)) -> Order:
    """Capture a payment and return the created order."""
    require_owner_or_admin(user, req.customer_id)
    with db.transaction() as conn:
        order_id = payments.capture(conn, user.id, req)
    return order_service.fetch_order(db.get_conn(), order_id, user)


@router.get("/{order_id}", response_model=Order)
def get_order(order_id: int, user: User = Depends(current_user)) -> Order:
    """Return a single order."""
    return order_service.fetch_order(db.get_conn(), order_id, user)
