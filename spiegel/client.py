from functools import wraps
from inspect import signature
import requests
from .utils import get_methods_on_class, get_properties_on_class


def client_method(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        self = args[0]
        # grab the signature of the original object method
        sig = signature(func)
        # bind the input arguments to the original signature
        params = sig.bind(*args, **kwargs)
        params = {k: v for k, v in params.arguments.items() if not k == "self"}
        # TODO func.__name__ coordinated with server
        # run a post request against the appropriate endpoint with the params
        print(f"triggered client method {func.__name__}.")
        ret = requests.post(f"{self.address}/{func.__name__}", json=params)
        return ret.json()
    return wrapped


def client_property(prop):
    @wraps(prop)
    def wrapped(self):
        # run a post request against the appropriate endpoint
        print(f"triggered client property {prop}.")
        ret = requests.post(f"{self.address}/{prop}")
        return ret.json()
    return wrapped


def create_client(cls, address):
    # copy the class
    class Client(cls):
        # does not have a traditional __init__ anymore, since it
        # connects to the already initialized remote object
        def __init__(self):
            pass

    methods = get_methods_on_class(cls)
    methods = [m for m in methods if not m.startswith("__")]
    properties = get_properties_on_class(cls)
    for name in methods:
        setattr(Client, name, client_method(getattr(Client, name)))
    for name in properties:
        setattr(Client, name, property(client_property(name)))
    setattr(Client, "address", address)
    return Client
