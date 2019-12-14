from _martinez import Contour
from hypothesis import given

from tests.utils import pickle_round_trip
from . import strategies


@given(strategies.contours)
def test_round_trip(contour: Contour) -> None:
    assert pickle_round_trip(contour) == contour
