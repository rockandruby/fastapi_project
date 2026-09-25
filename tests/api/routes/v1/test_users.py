from app.settings import API_V1_PREFIX
from tests.utils.user import create_user

def test_read_users(db_session, client):
    create_user(db_session)
    r = client.get(f"{API_V1_PREFIX}/users/")
    all_users = r.json()

    assert r.status_code == 200
    assert len(all_users) == 1

def test_create_user_noauth(client):
    r = client.post(f"{API_V1_PREFIX}/users/")

    assert r.status_code == 401

def test_create_user(client, skip_auth):
    data = {"name": "JohnD", "email": "johnd@test.com", "password": "123"}
    r = client.post(f"{API_V1_PREFIX}/users/",json=data)
    created_user = r.json()

    assert r.status_code == 200
    assert created_user["email"] == "johnd@test.com"

def test_show_user(db_session, client):
    user = create_user(db_session)
    r = client.get(f"{API_V1_PREFIX}/users/{user.id}")
    user = r.json()

    assert r.status_code == 200
    assert user["email"] == "foo@example.com"


def test_update_user_noauth(client):
    r = client.patch(f"{API_V1_PREFIX}/users/1")

    assert r.status_code == 401

def test_update_user(db_session, client, auth_header):
    user = create_user(db_session)
    data = {"name": "John2"}
    r = client.patch(f"{API_V1_PREFIX}/users/{user.id}", json=data, headers=auth_header(user.id))
    update_user = r.json()

    assert r.status_code == 200
    assert update_user["name"] == "John2"

def test_delete_user_noauth(client):
    r = client.delete(f"{API_V1_PREFIX}/users/1")

    assert r.status_code == 401

def test_delete_user(db_session, client, auth_header):
    user = create_user(db_session)
    client.delete(f"{API_V1_PREFIX}/users/{user.id}", headers=auth_header(user.id))
    r = client.get(f"{API_V1_PREFIX}/users/")
    all_users = r.json()

    assert r.status_code == 200
    assert len(all_users) == 0
