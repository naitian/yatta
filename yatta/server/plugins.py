"""Plugin manager"""

from dataclasses import dataclass
from importlib.metadata import entry_points

from pydantic import BaseModel

from yatta.server.dev import setup_frontend_dev


def get_plugins():
    """Get all plugins."""
    return {
        str(name): module.load()
        for name, module in dict(entry_points(group="yatta.plugins")).items()
    }


def setup_plugins():
    """Setup all plugins."""
    plugins = get_plugins()
    if len(plugins) == 0:
        return
    else:
        setup_frontend_dev()



@dataclass
class BaseComponent():
    """Base class for all components."""
    name: str
    props: BaseModel