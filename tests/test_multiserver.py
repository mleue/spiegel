from spiegel.multiserver import MultiServer
import pytest
from flask import Flask
from .calculator import Calculator


# TODO test that we can forward errors through the wire
# TODO test non-unique object ids


expected_endpoints = ["last_result", "sum"]
obj_ids = [1, 2, 3]


@pytest.fixture
def app():
    objs = [Calculator() for _ in range(3)]
    yield MultiServer(objs, obj_ids)


def test_server_returns_flask_app(app):
    assert isinstance(app, Flask)


def test_server_contains_expected_endpoints(app):
    endpoints = [rule.endpoint for rule in app.url_map.iter_rules()]
    for obj_id in obj_ids:
        for exp in expected_endpoints:
            assert f"{obj_id}.{exp}" in endpoints
    assert "ids" in endpoints


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client


def test_server_ids(client):
    r = client.post("/ids")
    assert r.json == obj_ids


def test_server_can_be_queried(client):
    for obj_id in obj_ids:
        r = client.post(f"/{obj_id}/last_result")
        assert r.status_code == 200
        assert r.json is None
        r = client.post(f"/{obj_id}/sum", json={"a": 1, "b": 2})
        assert r.status_code == 200
        assert r.json == 3
        r = client.post(f"/{obj_id}/last_result")
        assert r.status_code == 200
        assert r.json == 3


def test_server_fails_with_500_on_error(client):
    for obj_id in obj_ids:
        r = client.post(f"{obj_id}/sum", json={"a": 1, "b": "2"})
        assert r.status_code == 400
        assert r.json["type"] == "TypeError"
