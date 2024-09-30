import asyncio
from datetime import timedelta

import uvicorn
from quart import Quart, send_from_directory, websocket
from quart_auth import QuartAuth
from quart_schema import QuartSchema

from yatta.core import Yatta
from yatta.utils import SRC_DIR
from yatta.web.dev import SERVER_DEV_PORT

from .api import create_api


class Server:
    def __init__(
        self,
        yatta: Yatta,
        port=5000,
        host="0.0.0.0",
        hmr=False,
        secret_key: str | None = None,
        access_timeout: timedelta = timedelta(minutes=15),
        dev=False,
        vite_frontend=False,
    ):
        self.yatta = yatta
        self.host = host
        self.port = port
        self.dev = dev
        self.hmr = hmr
        self.vite_frontend = vite_frontend

        if secret_key is None:
            if not dev:
                raise ValueError("secret_key is required for production")
            secret_key = "dev_default_key"

        self.secret_key = secret_key
        self.access_timeout = access_timeout
        self.app = self.setup_app()

    def setup_app(self):
        api = create_api(self.yatta, self.secret_key, self.access_timeout)
        file_change_event = asyncio.Event()

        app = Quart(__name__)
        app.config["SECRET_KEY"] = self.secret_key
        QuartAuth(app)
        QuartSchema(app, openapi_path="/api/openapi.json")

        app.register_blueprint(api)

        if self.yatta.static_files is not None:
            for name, path in self.yatta.static_files.items():

                @app.route(f"/files/{name}/<path:fpath>")
                async def files(fpath: str):
                    return await send_from_directory(path, fpath)

        if not self.vite_frontend:

            @app.route("/assets/<path:fpath>")
            async def assets(fpath: str):
                return await send_from_directory(
                    SRC_DIR / "client" / "dist" / "assets", fpath
                )

            @app.route("/", defaults={"path": ""})
            @app.route("/<path:path>")
            async def all(path: str):
                print(path)
                return await send_from_directory(
                    SRC_DIR / "client" / "dist", "index.html"
                )
        else:
            self.port = SERVER_DEV_PORT

        if self.hmr:

            @app.websocket("/hmr")
            async def hmr():
                while True:
                    await file_change_event.wait()
                    await websocket.send("reload")
                    file_change_event.clear()

        @app.before_serving
        async def setup():
            if self.hmr:
                for component in self.yatta.task.values():
                    if component.dev:
                        asyncio.create_task(component.watch(file_change_event))

        return app

    def run(self):
        return self.run_dev() if self.dev else self.run_prod()

    def run_dev(self):
        with self.yatta.session():
            self.app.run(port=self.port, host=self.host, debug=True, use_reloader=True)

    def run_prod(self):
        with self.yatta.session():
            uvicorn.run(self.app, port=self.port)
