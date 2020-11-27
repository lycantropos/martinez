from hypothesis import given

from tests.bind_tests.hints import BoundBoundingBox
from tests.utils import pickle_round_trip
from . import strategies


@given(strategies.bounding_boxes)
def test_round_trip(bounding_box: BoundBoundingBox) -> None:
    assert pickle_round_trip(bounding_box) == bounding_box
