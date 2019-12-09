from spiegel.server import Server
import pytest
from flask import Flask
from .calculator import get_calculator


# TODO test that we can forward errors through the wire


expected_endpoints = ["obj.last_result", "obj.sum"]


@pytest.fixture
def app():
    yield Server(get_calculator(), get_calculator()())


def test_server_returns_flask_app(app):
    assert isinstance(app, Flask)


def test_server_contains_expected_endpoints(app):
    endpoints = [rule.endpoint for rule in app.url_map.iter_rules()]
    for exp in expected_endpoints:
        assert exp in endpoints


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client


def test_server_can_be_queried(client):
    r = client.post("/last_result")
    assert r.status_code == 200
    assert r.json is None
    r = client.post("/sum", json={"a": 1, "b": 2})
    assert r.status_code == 200
    assert r.json == 3
    r = client.post("/last_result")
    assert r.status_code == 200
    assert r.json == 3


def test_server_fails_with_500_on_error(client):
    r = client.post("/sum", json={"a": 1, "b": "2"})
    assert r.status_code == 500
