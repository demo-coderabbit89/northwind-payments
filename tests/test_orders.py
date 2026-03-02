from tests.conftest import ALICE, BOB, OPS


def test_owner_can_read_order(client, alice_order):
    r = client.get(f"/orders/{alice_order['id']}", headers=ALICE)
    assert r.status_code == 200
    assert r.json()["amount_cents"] == 5000


def test_other_customer_cannot_read_order(client, alice_order):
    assert client.get(f"/orders/{alice_order['id']}", headers=BOB).status_code == 404


def test_admin_can_read_any_order(client, alice_order):
    assert client.get(f"/orders/{alice_order['id']}", headers=OPS).status_code == 200


def test_capture_is_audited(client, alice_order):
    from app import db
    row = db.get_conn().execute("SELECT action FROM audit_log WHERE entity_id = ?", (alice_order["id"],)).fetchone()
    assert row["action"] == "capture"
