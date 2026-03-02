from fastapi import APIRouter, Depends, Query

from app import db
from app.auth import User, current_user
from app.models import Transaction, TransactionPage

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.get("", response_model=TransactionPage)
def list_transactions(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    user: User = Depends(current_user),
) -> TransactionPage:
    offset = (page - 1) * page_size
    sql = (
        "SELECT t.* FROM transactions t JOIN orders o ON o.id = t.order_id "
        "WHERE (? OR o.customer_id = ?) ORDER BY t.id LIMIT ? OFFSET ?"
    )
    rows = db.get_conn().execute(sql, (user.is_admin(), user.id, page_size, offset)).fetchall()
    return TransactionPage(items=[Transaction(**dict(r)) for r in rows], page=page, page_size=page_size)
