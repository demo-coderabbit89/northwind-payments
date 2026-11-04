from app import db
from app.auth import User
from app.services import ledger


def test_list_page_returns_page_metadata(client, alice_order):
    page = ledger.list_page(db.get_conn(), User(id=1, roles=frozenset({"customer"})), 1, 5)
    assert page.page == 1 and page.page_size == 5
