from fastapi import APIRouter, Depends, Query

from app import db
from app.auth import User, current_user
from app.models import TransactionPage
from app.services import ledger

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.get("", response_model=TransactionPage)
def list_transactions(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    user: User = Depends(current_user),
) -> TransactionPage:
    """List the caller's transactions, newest last."""
    return ledger.list_page(db.get_conn(), user, page, page_size)
