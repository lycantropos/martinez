import pickle

from _martinez import BoundingBox
from hypothesis import given

from . import strategies


@given(strategies.bounding_boxes)
def test_round_trip(bounding_box: BoundingBox) -> None:
    assert pickle.loads(pickle.dumps(bounding_box)) == bounding_box
