from functools import wraps
from inspect import signature
import requests
from .utils import get_relevant_attributes_from_class, return_is_exception
# TODO client can only connect if it has a matching version with the server


def client_method(method_name, method):
    @wraps(method)
    def wrapped(*args, **kwargs):
        self = args[0]
        # grab the signature of the original object method
        sig = signature(method)
        # bind the input arguments to the original signature
        params = sig.bind(*args, **kwargs)
        params = {k: v for k, v in params.arguments.items() if not k == "self"}
        # TODO func.__name__ coordinated with server
        # run a post request against the appropriate endpoint with the params
        ret = requests.post(f"{self.address}/{method_name}", json=params)
        ret = ret.json()
        # TODO add test that checks for this (i.e. doesn't raise error if return is list of words with those 2 words included)
        # TODO instead of ValueError, raise a SpiegelError here with all info
        if return_is_exception(ret):
            raise ValueError(ret["detail"]["message"])
        else:
            return ret
    return wrapped


def client_property(prop_name):
    @wraps(prop_name)
    def wrapped(self):
        # run a post request against the appropriate endpoint
        ret = requests.post(f"{self.address}/{prop_name}")
        ret = ret.json()
        if return_is_exception(ret):
            raise ValueError(ret["detail"]["message"])
        else:
            return ret
    return wrapped


def create_client(cls, address):
    # copy the class
    class Client(cls):
        # does not have a traditional __init__ anymore, since it
        # connects to the already initialized remote object
        def __init__(self):
            pass

    relevant_attributes = get_relevant_attributes_from_class(cls)
    for attr_name, attr in relevant_attributes:
        if callable(attr):
            setattr(Client, attr_name, client_method(attr_name, attr))
        elif isinstance(attr, property):
            setattr(Client, attr_name, property(client_property(attr_name)))
    setattr(Client, "address", address)
    return Client
