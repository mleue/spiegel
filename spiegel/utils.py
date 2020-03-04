from typing import Any
from inspect import signature, _empty
from pydantic import create_model, BaseModel

# TODO make this robust
# TODO write tests for this
# TODO get all public attributes on class/object?


def get_relevant_attributes_from_class(cls):
    relevant_attributes = []
    for attr_name, attr in vars(cls).items():
        # filter out magic methods
        if attr_name.startswith("__"):
            continue
        # take only methods and properties
        elif callable(attr) or isinstance(attr, property):
            relevant_attributes.append((attr_name, attr))
    return relevant_attributes


def create_pydantic_model_from_function_signature(func, uid):
    # grab the signature of the original object method
    sig = signature(func)
    # build a pydantic input model based on the function signature
    pydantic_params = {}
    for param_name, param in sig.parameters.items():
        # filter out the self parameter of the method
        if param_name == "self":
            continue
        else:
            param_type = (
                Any if param.annotation == _empty else param.annotation
            )
            param_default = ... if param.default == _empty else param.default
            pydantic_params[param_name] = (param_type, param_default)
    # need a unique name for each model here, otherwise openapi will complain
    return create_model(uid, **pydantic_params)


def is_dict(obj):
    return isinstance(obj, dict)


def contains_error_detail(ret):
    return is_dict(ret) and "detail" in ret and is_dict(ret["detail"])


def contains_error_fields(ret):
    return "type" in ret["detail"] and "message" in ret["detail"]


def return_is_exception(ret):
    return contains_error_detail(ret) and contains_error_fields(ret)


# TODO turn this into a class that can get dumped as json (to be transferred
# from server to client) but also instantiated and raised from a JSON response
class SpiegelError(ValueError):
    pass

class SpiegelWireError(SpiegelError):
    pass
