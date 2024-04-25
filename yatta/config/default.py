"""Default configuration file."""
import os
from datetime import timedelta


PORT=4000

# NOTE: you may want to use an absolute path here so as to prevent issues with
# accidentally operating on different databases by running the command from
# different directories.
DATABASE = "sqlite:///" + os.path.join(os.getcwd(), "yatta.db")

# NOTE: you must always change this!
SECRET_KEY = "super-secret-key"
ACCESS_TIMEOUT = timedelta(minutes=60 * 24 * 7)  # 1 week
