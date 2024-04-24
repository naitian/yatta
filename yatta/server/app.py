from typing import Union

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from yatta.server.settings import settings
from yatta.utils import SRC_DIR

app = FastAPI()


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"port": settings.port}


app.mount(
    "/",
    StaticFiles(directory=SRC_DIR / "client" / "dist", html=True),
    name="client",
)
