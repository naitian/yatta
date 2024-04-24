"""Default configuration file."""
import os


PORT=4000

# NOTE: you may want to use an absolute path here so as to prevent issues with
# accidentally operating on different databases by running the command from
# different directories.
DATABASE = "sqlite:///" + os.path.join(os.getcwd(), "yatta.db")
SECRET_KEY = "super-secret-key"
