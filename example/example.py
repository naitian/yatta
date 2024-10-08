from collections import OrderedDict
from yatta.core import Yatta
from yatta.utils import relative_path
from yatta.web import Server
from yatta.distributor import AllDistributor
from yatta.base import Textbox, TextDisplay, Checkboxes

yatta = Yatta(
    dataset=[
        {"text": "Hello, world!"},
        {"text": "Goodbye, world!"},
        {"text": "Hello, again!"},
        {"text": "Goodbye, again!"},
        {"text": "Hello, one more time!"},
    ],
    task=OrderedDict(
        {
            "text": TextDisplay(transform_fn=lambda x: x["text"], dev=True),
            "annotation": Textbox(placeholder="Type notes here..."),
            "choices": Checkboxes(choices=["Hello", "Goodbye"], dev=True),
        }
    ),
    distributor=AllDistributor,
    ordering=iter,
    static_files={
        "cats": relative_path("./cat_files")  # serve files from the cat_files directory
    },
)

with yatta.session():
    yatta.assign_tasks()
    yatta.assign_all_orderings()

server = Server(yatta, port=5000, secret_key="very_secret_key", dev=True, hmr=True)
server.run()
