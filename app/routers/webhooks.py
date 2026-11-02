from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.auth import User, current_user
from app.services import webhooks

router = APIRouter(prefix="/webhooks", tags=["webhooks"])


class Subscription(BaseModel):
    url: str


@router.post("", status_code=201)
def create_subscription(sub: Subscription, user: User = Depends(current_user)):
    webhooks.subscribe(sub.url)
    return {"subscribed": sub.url}
