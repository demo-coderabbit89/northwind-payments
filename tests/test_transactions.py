from tests.conftest import ALICE


def test_first_page_starts_at_first_transaction(client, alice_order):
    r = client.get("/transactions?page=1&page_size=10", headers=ALICE)
    assert r.status_code == 200
    assert [t["order_id"] for t in r.json()["items"]] == [alice_order["id"]]


def test_transaction_amounts_are_in_dollars(client, alice_order):
    r = client.get("/transactions", headers=ALICE)
    assert r.json()["items"][0]["amount"] == 50.0
