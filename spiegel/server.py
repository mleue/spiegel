from typing import Any
from fastapi import FastAPI, HTTPException, APIRouter
from .utils import (
    get_relevant_attributes_from_class,
    create_pydantic_model_from_function_signature,
)


# TODO also create a return Model based on the return annotation of the func
def create_method_endpoint(obj, method_name, method):
    # need a uid for each pydantic model, otherwise openapi complains
    uid = f"{method_name}.{id(obj)}"
    Model = create_pydantic_model_from_function_signature(method, uid)
    def wrapped(i: Model):
        # call the original attr on the true object with the parsed args
        try:
            return method(obj, **i.dict())
        except Exception as e:
            payload = {"type": type(e).__name__, "message": str(e)}
            raise HTTPException(400, payload)
    return wrapped


def create_property_endpoint(obj, prop_name, prop):
    def wrapped():
        # call the original property getter on the true object
        try:
            return getattr(obj, prop_name)
        except Exception as e:
            payload = {"type": type(e).__name__, "message": str(e)}
            raise HTTPException(400, payload)
    return wrapped


def create_obj_router(obj):
    cls = obj.__class__
    relevant_attributes = get_relevant_attributes_from_class(cls)
    router = APIRouter()
    for attr_name, attr in relevant_attributes:
        if callable(attr):
            endpoint = create_method_endpoint(obj, attr_name, attr)
        elif isinstance(attr, property):
            endpoint = create_property_endpoint(obj, attr_name, attr)
        router.add_api_route(f"/{attr_name}", endpoint, methods=["POST"])
    return router


def create_server(obj):
    router = create_obj_router(obj)
    app = FastAPI()
    app.include_router(router)
    return app
