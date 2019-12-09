from flask import Flask
from .server import create_obj_blueprint


def MultiServer(classes, objs, obj_ids):
    app = Flask(__name__)
    for cls, obj, obj_id in zip(classes, objs, obj_ids):
        url_prefix = f"/{obj_id}"
        bp = create_obj_blueprint(cls, obj, obj_id, url_prefix)
        app.register_blueprint(bp)
    return app
