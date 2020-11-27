from hypothesis import given

from tests.bind_tests.hints import BoundContour
from tests.utils import pickle_round_trip
from . import strategies


@given(strategies.contours)
def test_round_trip(contour: BoundContour) -> None:
    assert pickle_round_trip(contour) == contour
