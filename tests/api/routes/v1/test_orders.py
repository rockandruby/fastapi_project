from app.settings import API_V1_PREFIX
from tests.utils.order import create_order
from tests.utils.user import create_user

def test_read_orders_noauth(client):
    r = client.get(f"{API_V1_PREFIX}/orders/")

    assert r.status_code == 401


def test_read_orders(db_session, client, auth_header):
    user = create_user(db_session)
    create_order(db_session, user)
    r = client.get(f"{API_V1_PREFIX}/orders/", headers=auth_header(user.id))
    all_orders = r.json()

    assert r.status_code == 200
    assert len(all_orders) == 1

def test_show_order_noauth(client):
    r = client.get(f"{API_V1_PREFIX}/orders/1")

    assert r.status_code == 401

def test_show_order(db_session, client, auth_header):
    user = create_user(db_session)
    created_order = create_order(db_session, user)
    r = client.get(f"{API_V1_PREFIX}/orders/{created_order.id}", headers=auth_header(user.id))
    order = r.json()

    assert r.status_code == 200
    assert created_order.title == order["title"]


def test_update_order_noauth(client):
    r = client.patch(f"{API_V1_PREFIX}/orders/1")

    assert r.status_code == 401


def test_update_order(db_session, client, auth_header):
    user = create_user(db_session)
    created_order = create_order(db_session, user)
    data = {"title": "New order title"}
    r = client.patch(f"{API_V1_PREFIX}/orders/{created_order.id}", json=data, headers=auth_header(user.id))
    order = r.json()

    assert r.status_code == 200
    assert data["title"] == order["title"]

def test_delete_order_noauth(client):
    r = client.delete(f"{API_V1_PREFIX}/orders/1")

    assert r.status_code == 401


def test_delete_order(db_session, client, auth_header):
    user = create_user(db_session)
    created_order = create_order(db_session, user)
    r = client.delete(f"{API_V1_PREFIX}/orders/{created_order.id}", headers=auth_header(user.id))

    assert r.status_code == 200
