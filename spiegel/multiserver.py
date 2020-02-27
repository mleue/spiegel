from fastapi import FastAPI
from .server import create_obj_router

# TODO auto-generate object ids?
# TODO not just /ids but also a more verbose /objects endpoint


def MultiServer(objs, obj_ids):
    app = FastAPI(__name__)
    for obj, obj_id in zip(objs, obj_ids):
        router = create_obj_router(obj)
        app.include_router(router, prefix=f"/{obj_id}")
    app.add_api_route("/ids", lambda: obj_ids, methods=["POST"])
    return app
