import time
import threading
from spiegel.client import create_client
from spiegel.server import create_server
import pytest
from .calculator import Calculator


# TODO test that altered class methods/properties have same signature as orig


@pytest.fixture(scope="session")
def app():
    yield create_server(Calculator())


@pytest.fixture(scope="session")
def model_server(app):
    thread = threading.Thread(target=app.run, kwargs={"port": 5000})
    thread.daemon = True
    thread.start()
    time.sleep(0.1)


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
