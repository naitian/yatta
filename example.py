from yatta.core import Yatta
from yatta.web import Server
from yatta.distributor import AllDistributor
from yatta.base import Textbox

yatta = Yatta(
    dataset=[
        {"text": "Hello, world!"},
        {"text": "Goodbye, world!"},
        {"text": "Hello, again!"},
        {"text": "Goodbye, again!"},
        {"text": "Hello, one more time!"},
    ],
    task={"text": Textbox(transform_fn=lambda x: x["text"], placeholder="Type here...")},
    distributor=AllDistributor,
    ordering=iter,
)

with yatta.session():
    yatta.assign_tasks()
    yatta.assign_all_orderings()

server = Server(yatta, port=5000, secret_key="very_secret_key", dev=True)
server.run()
