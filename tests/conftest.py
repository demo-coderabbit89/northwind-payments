import pytest
from fastapi.testclient import TestClient

from app import db
from app.main import app

ALICE = {"Authorization": "Bearer token-alice"}
BOB = {"Authorization": "Bearer token-bob"}
OPS = {"Authorization": "Bearer token-ops"}


@pytest.fixture()
def client():
    db.set_conn(db.connect(":memory:"))
    with TestClient(app) as c:
        yield c


@pytest.fixture()
def alice_order(client):
    r = client.post("/orders", json={"customer_id": 1, "amount_cents": 5000, "card_last4": "4242"}, headers=ALICE)
    assert r.status_code == 201
    return r.json()
