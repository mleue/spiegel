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


def create_pydantic_model_from_function_signature(name, func):
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
    return create_model(name, **pydantic_params)
