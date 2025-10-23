import pytest
from app import app as a
from ..utils import db
import json


@pytest.fixture
def app():
    with a.app_context():
        db.create_all()
        yield a
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def test_register_and_login_and_create_recipe(client):
    # register
    r = client.post("/register", json={"username": "alice", "password": "pass"})
    assert r.status_code == 201

    # login
    r = client.post("/login", json={"username": "alice", "password": "pass"})
    assert r.status_code == 200
    token = r.get_json()["access_token"]
    assert token

    # create recipe
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "title": "Toast",
        "description": "Simple toast",
        "ingredients": "bread, butter",
        "instructions": "Toast bread, add butter.",
    }
    r = client.post("/recipes", json=payload, headers=headers)
    assert r.status_code == 201
    data = r.get_json()
    assert "id" in data

    # list recipes
    r = client.get("/recipes")
    assert r.status_code == 200
    lst = r.get_json()
    assert len(lst) == 1
    assert lst[0]["title"] == "Toast"
