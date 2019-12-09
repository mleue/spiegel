import requests
from .client import Client


class MultiClient:
    def __init__(self, cls_factory, address):
        self.cls_factory = cls_factory
        self.address = address

    @property
    def ids(self):
        return requests.post(f"{self.address}/ids").json()

    def create_client_for_id(self, obj_id):
        return Client(self.cls_factory(), f"{self.address}/{obj_id}")
