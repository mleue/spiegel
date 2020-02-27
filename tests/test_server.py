from spiegel.server import create_server
import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient
from .calculator import Calculator


# TODO test that we can forward errors through the wire


expected_endpoints = ["/last_result", "/sum", "/quotient"]


@pytest.fixture
def app():
    yield create_server(Calculator())


def test_server_returns_fastapi_app(app):
    assert isinstance(app, FastAPI)


def test_server_contains_expected_endpoints(app):
    endpoints = [route.path for route in app.routes]
    for exp in expected_endpoints:
        assert exp in endpoints


@pytest.fixture
def client(app):
    yield TestClient(app)


def test_server_can_be_queried(client):
    r = client.post("/last_result")
    assert r.status_code == 200
    assert r.json() is None
    r = client.post("/sum", json={"a": 1, "b": 2})
    assert r.status_code == 200
    assert r.json() == 3
    r = client.post("/last_result")
    assert r.status_code == 200
    assert r.json() == 3


def test_server_fails_with_422_on_input_validation_error(client):
    r = client.post("/sum", json={"a": 1, "b": "abc"})
    assert r.status_code == 422
    assert r.json()["detail"][0]["msg"] == "value is not a valid float"
    assert r.json()["detail"][0]["type"] == "type_error.float"


def test_server_method_raises_exception(client):
    r = client.post("/quotient", json={"a": 1, "b": 0})
    assert r.json()["detail"]["type"] == "ZeroDivisionError"
    assert r.json()["detail"]["message"] == "float division by zero"
