from inspect import signature
from flask import Flask, request, Blueprint
from flask.json import jsonify
from .utils import get_methods_on_class, get_properties_on_class


def server_method(func, obj):
    def wrapped(*args, **kwargs):
        # grab the signature of the original object method
        sig = signature(func)
        # according to the signature, parse all expected arguments
        # from the request payload
        forward_kwargs = {}
        for name, _ in sig.parameters.items():
            if not name == "self":
                forward_kwargs[name] = request.json.get(name)
        # call the original method on the true object with the parsed args
        ret = getattr(obj, func.__name__)(**forward_kwargs)
        return jsonify(ret)

    return wrapped


def server_property(prop, obj):
    def wrapped():
        # call the original property getter on the true object
        ret = getattr(obj, prop)
        return jsonify(ret)

    return wrapped


def create_obj_blueprint(cls, obj, obj_id, url_prefix=None):
    bp = Blueprint(obj_id, __name__, url_prefix=url_prefix)
    methods = get_methods_on_class(cls)
    methods = [m for m in methods if not m.startswith("__")]
    properties = get_properties_on_class(cls)
    # TODO remove duplication
    for mname in methods:
        bp.add_url_rule(
            f"/{mname}",
            mname,
            server_method(getattr(cls, mname), obj),
            methods=["POST"],
        )
    for pname in properties:
        bp.add_url_rule(
            f"/{pname}", pname, server_property(pname, obj), methods=["POST"],
        )
    return bp


# TODO make it so that only the obj is required?
def Server(cls, obj):
    app = Flask(__name__)
    bp = create_obj_blueprint(cls, obj, obj_id="obj")
    app.register_blueprint(bp)
    return app
