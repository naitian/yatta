"""Default configuration file."""

from collections.abc import Sequence
from pathlib import Path

from pydantic import BaseModel, ConfigDict
from datetime import timedelta

from yatta.distributor import Distributor, AllDistributor, RoundRobinDistributor
from yatta.ordering import DataOrdering, SequentialOrdering
from yatta.server.plugins import Component


class Settings(BaseModel):
    port: int = 4000
    is_dev: bool = False
    dataset: Sequence | None = None
    static_files: dict[str, str | Path] = {}

    task: dict[str, Component] = {}

    data_distributors: dict[str, Distributor] = {
        "all": AllDistributor,
        "round_robin": RoundRobinDistributor,
    }
    ordering: DataOrdering = SequentialOrdering


    # NOTE: you must always change this!
    secret_key: str = "super-secret-key"
    access_timeout: timedelta = timedelta(hours=1)

    db_name: str = "yatta.db"

    # NOTE: you may want to use an absolute path for database so as to prevent
    # issues with accidentally operating on different databases by running the
    # command from different directories.
    # defaults to "sqlite:///" + os.path.join(os.getcwd(), settings.db_name)
    database: str | None = None

    model_config: ConfigDict = {"arbitrary_types_allowed": True}


default = Settings()
