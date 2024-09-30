from datetime import timedelta

from quart_auth import QuartAuth
from quart_schema import QuartSchema
import uvicorn
from quart import Quart, send_from_directory

from yatta.core import Yatta
from yatta.utils import SRC_DIR
from yatta.web.dev import SERVER_DEV_PORT, run_frontend_dev, setup_frontend_dev

from .api import create_api


# class BaizeStaticFiles(Files):
#     def __call__(self, scope, receive, send):
#         scope["path"] = os.path.relpath(scope["path"], scope["root_path"])
#         return super().__call__(scope, receive, send)


# class SPAStaticFiles(StaticFiles):
#     async def get_response(self, path: str, scope):
#         try:
#             return await super().get_response(path, scope)
#         except (HTTPException, StarletteHTTPException) as ex:
#             if ex.status_code == 404:
#                 return await super().get_response("index.html", scope)
#             else:
#                 raise ex


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

        app = Quart(__name__)
        app.config["SECRET_KEY"] = self.secret_key
        QuartAuth(app)
        QuartSchema(app, openapi_path="/api/openapi.json")

        app.register_blueprint(api)

        # def handle(scope, receive, send):
        #     filepath = scope["path"]
        #     print(filepath)
        #     raise HTTPException(404)

        if self.yatta.static_files is not None:
            for name, path in self.yatta.static_files.items():
                # static = FastAPI()
                # static.mount(
                #     "/", BaizeStaticFiles(directory=path, handle_404=handle), name=name
                # )
                @app.route(f"/files/{name}/<path:fpath>")
                async def files(fpath: str):
                    return await send_from_directory(path, fpath)

        if not self.dev:

            @app.route("/", defaults={"path": ""})
            @app.route("<path:path>")
            async def all():
                return await send_from_directory(
                    SRC_DIR / "client" / "dist", "index.html"
                )

        return app

    def run(self):
        return self.run_dev() if self.dev else self.run_prod()

    def run_dev(self):
        if not setup_frontend_dev():
            return
        # run_frontend_dev(port=self.port)

        with self.yatta.session():
            self.app.run(
                port=SERVER_DEV_PORT, host=self.host, debug=True, use_reloader=True
            )

    def run_prod(self):
        with self.yatta.session():
            uvicorn.run(self.app, port=self.port)
