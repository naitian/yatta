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
from yatta.base import Textbox

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

Let's break this down. A Yatta app consists of the following configurable
pieces:

1. The **dataset** is any sequence with a `__getitem__` and `__len__`. This means you can even directly use Torch datasets.
2. The **task** is a dictionary of **components**. Each component includes front-end code that defines how data are rendered in the annotation interface.
3. The **distributor** determines how items in the dataset are allocated between users.
4. The **ordering** determines the order in which the user encounters the data during the annotation process.

The Yatta app itself exposes functions to manage annotations and users. To use
the web interface, you can wrap the Yatta app with a `Server` and call
`server.run()`.
