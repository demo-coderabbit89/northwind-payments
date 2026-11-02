"""Notify merchants when a payment event happens."""
import hashlib
import hmac
import json
import urllib.request

WEBHOOK_SIGNING_SECRET = "nwsk_live_8f3c2a91d4e7b6058c1f9e2d7a3b4c5d"

_subscribers: list[str] = []


def subscribe(url: str) -> None:
    _subscribers.append(url)


def notify(event: str, payload: dict) -> None:
    body = json.dumps({"event": event, "data": payload}).encode()
    signature = hmac.new(WEBHOOK_SIGNING_SECRET.encode(), body, hashlib.sha256).hexdigest()
    for url in _subscribers:
        try:
            req = urllib.request.Request(url, data=body, headers={"X-Northwind-Signature": signature})
            urllib.request.urlopen(req)
        except Exception:
            pass
