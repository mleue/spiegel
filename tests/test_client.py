import time
from multiprocessing import Process
import pytest
import uvicorn
from spiegel.client import create_client
from spiegel.server import create_server
from .calculator import Calculator


# TODO test that altered class methods/properties have same signature as orig


@pytest.fixture(scope="session")
def app():
    yield create_server(Calculator())


@pytest.fixture(scope="session")
def model_server(app):
    p = Process(target=uvicorn.run, args=(app,), kwargs={"port": 5000}, daemon=True)
    p.start()
    time.sleep(0.1)
    yield
    p.kill()


@pytest.fixture(scope="session")
def client(model_server):
    yield create_client(Calculator, "http://localhost:5000")()


def test_client_returns_original_class_type(client):
    assert isinstance(client, Calculator)


def test_client_can_be_used(client):
    assert client.last_result is None
    assert client.sum(1, 2) == 3
    assert client.last_result == 3


# TODO handle error cases by error exception pass-through
@pytest.mark.xfail
def test_client_fails_on_error(client):
    client.sum(1, "2")
