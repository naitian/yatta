# Yatta

> Yet AnoTher Tool for Annotation

Yatta is a flexible framework for creating annotation tools that abstracts away
the boring bits (user and data management) so that you can focus on quickly
creating complex annotation interfaces.

## Quickstart

Your Yatta app is as simple as a single Python file.

```py
from yatta.core import Yatta
from yatta.web import Server
from yatta.distributor import AllDistributor
from yatta.ordering import SequentialOrdering
from yatta.base.textbox import Textbox

yatta = Yatta(
    dataset=[
        {"text": "Hello, world!"},
        {"text": "Goodbye, world!"},
        {"text": "Hello, again!"},
        {"text": "Goodbye, again!"},
        {"text": "Hello, one more time!"},
    ],
    task={"text": Textbox()},
    distributor=AllDistributor,
    ordering=SequentialOrdering,
)

with yatta.session():
    yatta.assign_tasks()
    yatta.assign_all_orderings()

server = Server(yatta, port=5000, secret_key="very_secret_key")
server.run()
```

This will create a web app that runs on port 5000.