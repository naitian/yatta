import anywidget
import traitlets

from yatta.core import Yatta
from yatta.core.models import AnnotationAssignmentResponse, AnnotationObject, User
from yatta.utils import SRC_DIR
from yatta.web.api import format_annotation_datum


class YattaWidget(anywidget.AnyWidget):
    _esm = SRC_DIR / "client" / "jupyter" / "jupyter.js"
    _css = SRC_DIR / "client" / "jupyter" / "style.css"
    # _esm = "http://localhost:4173/jupyter.js?hi"

    datum = traitlets.Int(0).tag(sync=True)
    task = traitlets.Dict({}).tag(sync=True)
    assignment = traitlets.Dict({}).tag(sync=True)
    result = traitlets.Dict({}).tag(sync=True)

    def get_annotation(self):
        assignment = self.yatta.get_annotation(self.user, self.datum)
        datum = self.yatta.dataset[self.datum]
        return AnnotationAssignmentResponse(
            components=format_annotation_datum(self.yatta, datum, assignment),
            is_complete=assignment.is_complete,
            is_skipped=assignment.is_skipped,
            next=assignment.next,
            prev=assignment.prev,
        ).model_dump()

    def __init__(self, yatta: Yatta, user: User, **kwargs):
        super().__init__(**kwargs)
        self.yatta = yatta
        self.user = user
        self.task = self.yatta.get_task()
        self.assignment = self.get_annotation()

    def set_datum(self, change):
        self.assignment = self.get_annotation()

    @traitlets.observe("result")
    def on_change(self, change):
        with self.yatta.session():
            self.yatta.set_annotation(
                self.user, self.datum, AnnotationObject(**change["new"])
            )
            self.assignment = self.get_annotation()
