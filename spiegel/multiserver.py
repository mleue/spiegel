from fastapi import FastAPI, APIRouter, HTTPException
from .server import create_obj_router

# TODO auto-generate object ids?
# TODO not just /ids but also a more verbose /objects endpoint (like the /models we now do on neuromodels)
# TODO why is single client a clear function but this looks like a class?
# TODO instead of fixed paths for each id, make a dynamic path operation that calls the correct object?


def MultiServer(objs, obj_ids):
    root_router = APIRouter()
    for obj, obj_id in zip(objs, obj_ids):
        router = create_obj_router(obj)
        root_router.include_router(router, prefix=f"/{obj_id}")
    root_router.add_api_route("/ids", lambda: obj_ids, methods=["POST"])
    app = FastAPI()
    app.include_router(root_router)
    return app
