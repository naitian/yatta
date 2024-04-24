from typing import Union

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from yatta.utils import relative_path

app = FastAPI()


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


app.mount(
    "/",
    StaticFiles(directory=relative_path("../client/dist/"), html=True),
    name="client",
)
