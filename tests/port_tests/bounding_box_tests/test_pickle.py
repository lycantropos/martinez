import pickle

from hypothesis import given

from martinez.bounding_box import BoundingBox
from . import strategies


@given(strategies.bounding_boxes)
def test_round_trip(bounding_box: BoundingBox) -> None:
    assert pickle.loads(pickle.dumps(bounding_box)) == bounding_box
