from yatta.config.default import *  # noqa: F403, F401
from yatta.dataset.dsv import DSVDataset


DATASET = DSVDataset("./tests/simple.csv")


def render_datum(datum):
    return f"{datum['other_label']}: <i>{datum['text']}</i>"

DATA_RENDER = render_datum
