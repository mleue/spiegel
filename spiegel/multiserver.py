from flask import Flask, Blueprint
from flask.json import jsonify
from .server import create_obj_blueprint

# TODO auto-generate object ids?
# TODO not just /ids but also a more verbose /objects endpoint


def MultiServer(objs, obj_ids):
    app = Flask(__name__)
    for obj, obj_id in zip(objs, obj_ids):
        url_prefix = f"/{obj_id}"
        bp = create_obj_blueprint(obj, obj_id, url_prefix)
        app.register_blueprint(bp)
    app.add_url_rule("/ids", "ids", lambda: jsonify(obj_ids), methods=["POST"])
    return app
