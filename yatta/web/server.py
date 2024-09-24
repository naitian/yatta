import asyncio
import os
from datetime import timedelta

from baize.asgi import Files
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from hypercorn.asyncio import serve
from hypercorn.config import Config
from starlette.exceptions import HTTPException as StarletteHTTPException

from yatta.core import Yatta
from yatta.utils import SRC_DIR
from yatta.web.dev import SERVER_DEV_PORT, run_frontend_dev, setup_frontend_dev

from .api import create_api


class BaizeStaticFiles(Files):
    def __call__(self, scope, receive, send):
        scope["path"] = os.path.relpath(scope["path"], scope["root_path"])
        return super().__call__(scope, receive, send)


class SPAStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope):
        try:
            return await super().get_response(path, scope)
        except (HTTPException, StarletteHTTPException) as ex:
            if ex.status_code == 404:
                return await super().get_response("index.html", scope)
            else:
                raise ex


class Server:
    def __init__(
        self,
        yatta: Yatta,
        port=5000,
        host="0.0.0.0",
        secret_key: str | None = None,
        access_timeout: timedelta = timedelta(minutes=15),
        dev=False,
    ):
        self.yatta = yatta
        self.host = host
        self.port = port
        self.dev = dev

        if secret_key is None:
            if not dev:
                raise ValueError("secret_key is required for production")
            secret_key = "dev_default_key"

        self.secret_key = secret_key
        self.access_timeout = access_timeout
        self.app = self.setup_app()

    def setup_app(self):
        api = create_api(self.yatta, self.secret_key, self.access_timeout)

        app = FastAPI()

        def handle(scope, receive, send):
            filepath = scope["path"]
            print(filepath)
            raise HTTPException(404)

        if self.yatta.static_files is not None:
            for name, path in self.yatta.static_files.items():
                static = FastAPI()
                static.mount(
                    "/", BaizeStaticFiles(directory=path, handle_404=handle), name=name
                )
                app.mount(f"/files/{name}/", static)

        app.include_router(api)
        if not self.dev:
            app.mount(
                "/",
                SPAStaticFiles(
                    directory=SRC_DIR / "client" / "dist", html=True, check_dir=False
                ),
                name="client",
            )
        return app

    def run(self):
        return self.run_dev() if self.dev else self.run_prod()

    def run_dev(self):
        if not setup_frontend_dev():
            return
        run_frontend_dev(port=self.port)
        config = Config()
        config.bind = [f"{self.host}:{SERVER_DEV_PORT}"]
        config.use_reloader = True

        with self.yatta.session():
            asyncio.run(serve(self.app, config))  # type: ignore

    def run_prod(self):
        config = Config()
        config.bind = [f"{self.host}:{self.port}"]
        with self.yatta.session():
            asyncio.run(serve(self.app, config))  # type: ignore
