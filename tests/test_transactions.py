from tests.conftest import ALICE, BOB


def test_first_page_starts_at_first_transaction(client, alice_order):
    r = client.get("/transactions?page=1&page_size=10", headers=ALICE)
    assert r.status_code == 200
    assert [t["order_id"] for t in r.json()["items"]] == [alice_order["id"]]


def test_customers_only_see_their_transactions(client, alice_order):
    assert client.get("/transactions", headers=BOB).json()["items"] == []
