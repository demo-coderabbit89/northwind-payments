"""API models."""
from pydantic import BaseModel, Field


class Order(BaseModel):
    id: int
    customer_id: int
    amount: float
    currency: str
    card_last4: str
    status: str


class Transaction(BaseModel):
    id: int
    order_id: int
    kind: str
    amount: float
    created_at: str


class TransactionPage(BaseModel):
    items: list[Transaction]
    page: int
    page_size: int


class CaptureRequest(BaseModel):
    customer_id: int
    amount_cents: int = Field(gt=0)
    currency: str = "USD"
    card_last4: str = Field(pattern=r"^\d{4}$")
