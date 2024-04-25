"""Default configuration file."""

import os
from datetime import timedelta

from yatta.distributor import AllDistributor, RoundRobinDistributor

PORT = 4000

# NOTE: you may want to use an absolute path here so as to prevent issues with
# accidentally operating on different databases by running the command from
# different directories.
DB_NAME = "yatta.db"
DATABASE = None  # defaults to "sqlite:///" + os.path.join(os.getcwd(), settings.db_name)

# NOTE: you must always change this!
SECRET_KEY = "super-secret-key"
ACCESS_TIMEOUT = timedelta(hours=1)

DATA_DISTRIBUTORS = {"all": AllDistributor, "round_robin": RoundRobinDistributor}
