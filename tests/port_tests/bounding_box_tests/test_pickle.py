from hypothesis import given

from tests.port_tests.hints import PortedBoundingBox
from tests.utils import pickle_round_trip
from . import strategies


@given(strategies.bounding_boxes)
def test_round_trip(bounding_box: PortedBoundingBox) -> None:
    assert pickle_round_trip(bounding_box) == bounding_box
