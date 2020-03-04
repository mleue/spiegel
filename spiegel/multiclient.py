import requests
from .client import create_client
from .utils import SpiegelError


class MultiClient:
    def __init__(self, cls, address):
        self.cls = cls
        self.address = address

    @property
    def ids(self):
        return requests.post(f"{self.address}/ids").json()

    def create_client_for_id(self, obj_id):
        if obj_id not in self.ids:
            raise SpiegelError(f"Object {obj_id} does not exist.")
        else:
            return create_client(self.cls, f"{self.address}/{obj_id}")
