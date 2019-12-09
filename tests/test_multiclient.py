import time
import threading
from spiegel.multiclient import MultiClient
from spiegel.multiserver import MultiServer
import pytest
from .calculator import Calculator


obj_ids = [1, 2, 3]


@pytest.fixture(scope="session")
def app():
    objs = [Calculator() for _ in range(3)]
    yield MultiServer(objs, obj_ids)


@pytest.fixture(scope="session")
def model_server(app):
    thread = threading.Thread(target=app.run, kwargs={"port": 5001})
    thread.daemon = True
    thread.start()
    time.sleep(0.1)


@pytest.fixture(scope="session")
def client(model_server):
    yield MultiClient(Calculator, "http://localhost:5001")


@pytest.mark.xfail
def test_client_returns_original_class_type(client):
    assert isinstance(client, Calculator)


def test_client_can_get_ids(client):
    assert client.ids == obj_ids


def test_client_can_be_used(client):
    for obj_id in obj_ids:
        obj_client = client.create_client_for_id(obj_id)()
        assert obj_client.last_result is None
        assert obj_client.sum(1, 2) == 3
        assert obj_client.last_result == 3


# TODO handle error cases by error exception pass-through
@pytest.mark.xfail
def test_client_fails_on_error(client):
    obj_client = client.create_client_for_id(1)
    client.sum(1, "2")
