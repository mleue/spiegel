from spiegel.multiserver import MultiServer
import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient
from .calculator import Calculator


# TODO test that we can forward errors through the wire
# TODO test non-unique object ids


expected_endpoints = ["last_result", "sum"]
obj_ids = [1, 2, 3]


@pytest.fixture
def app():
    objs = [Calculator() for _ in range(3)]
    yield MultiServer(objs, obj_ids)


def test_server_returns_fastapi_app(app):
    assert isinstance(app, FastAPI)


def test_server_contains_expected_endpoints(app):
    endpoints = [route.path for route in app.routes]
    for obj_id in obj_ids:
        for exp in expected_endpoints:
            assert f"/{obj_id}/{exp}" in endpoints
    assert "/ids" in endpoints


@pytest.fixture
def client(app):
    yield TestClient(app)


def test_server_ids(client):
    r = client.post("/ids")
    assert r.json() == obj_ids


def test_server_can_be_queried(client):
    for obj_id in obj_ids:
        r = client.post(f"/{obj_id}/last_result")
        assert r.status_code == 200
        assert r.json() is None
        r = client.post(f"/{obj_id}/sum", json={"a": 1, "b": 2})
        assert r.status_code == 200
        assert r.json() == 3
        r = client.post(f"/{obj_id}/last_result")
        assert r.status_code == 200
        assert r.json() == 3


def test_server_fails_with_422_on_input_validation_error(client):
    for obj_id in obj_ids:
        r = client.post(f"{obj_id}/sum", json={"a": 1, "b": "abc"})
        assert r.status_code == 422
        assert r.json()["detail"][0]["msg"] == "value is not a valid float"
        assert r.json()["detail"][0]["type"] == "type_error.float"
