from inspect import signature, _empty
from pydantic import create_model
from fastapi import FastAPI, HTTPException, APIRouter
from .utils import get_methods_on_class, get_properties_on_class


def server_method(func, obj):
    # grab the signature of the original object method
    sig = signature(func)
    # build a pydantic input model based on the function signature
    pydantic_params = {}
    for param_name, param in sig.parameters.items():
        if param_name == "self":
            continue
        else:
            param_type = (
                Any if param.annotation == _empty else param.annotation
            )
            param_default = ... if param.default == _empty else param.default
            pydantic_params[param_name] = (param_type, param_default)
    ModelIn = create_model(func.__name__, **pydantic_params)

    def wrapped(i: ModelIn):
        # call the original method on the true object with the parsed args
        try:
            return getattr(obj, func.__name__)(**i.dict())
        except Exception as e:
            payload = {"type": type(e).__name__, "message": str(e)}
            return HTTPException(400, payload)

    return wrapped


def server_property(prop, obj):
    def wrapped():
        # call the original property getter on the true object
        try:
            return getattr(obj, prop)
        except Exception as e:
            payload = {"type": type(e).__name__, "message": str(e)}
            return HTTPException(400, payload)

    return wrapped


def create_obj_router(obj):
    cls = obj.__class__
    router = APIRouter()
    methods = get_methods_on_class(cls)
    methods = [m for m in methods if not m.startswith("__")]
    properties = get_properties_on_class(cls)
    # TODO remove duplication
    for mname in methods:
        router.add_api_route(
            f"/{mname}",
            server_method(getattr(cls, mname), obj),
            methods=["POST"],
        )
    for pname in properties:
        router.add_api_route(
            f"/{pname}", server_property(pname, obj), methods=["POST"],
        )
    return router


def create_server(obj):
    router = create_obj_router(obj)
    app = FastAPI(__name__)
    app.include_router(router)
    return app
