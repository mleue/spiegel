from functools import wraps
from inspect import signature
import requests
from .utils import get_methods_and_properties


def client_method(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        # grab the signature of the original object method
        sig = signature(func)
        # bind the input arguments to the original signature
        params = sig.bind(*args, **kwargs)
        params = {k: v for k, v in params.arguments.items() if not v == "self"}
        # TODO func.__name__ coordinated with server
        # run a post request against the appropriate endpoint with the params
        ret = requests.post(f"{address}/{func.__name__}", json=params)
        return ret.json()
    return wrapped


def client_property(prop):
    @wraps(prop)
    def wrapped(self):
        # run a post request against the appropriate endpoint
        ret = requests.post(f"{address}/{prop}")
        return ret.json()
    return wrapped


def Client(cls):
    # TODO replace __init__ method to allow specification of address
    methods, properties = get_methods_and_properties(cls)
    methods = [m for m in methods if not m.startswith("__")]
    for name in methods:
        setattr(cls, name, client_method(getattr(cls, name)))
    for name in properties:
        setattr(cls, name, property(client_property(name)))
    return cls