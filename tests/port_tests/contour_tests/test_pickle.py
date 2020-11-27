from hypothesis import given

from tests.port_tests.hints import PortedContour
from tests.utils import pickle_round_trip
from . import strategies


@given(strategies.contours)
def test_round_trip(contour: PortedContour) -> None:
    assert pickle_round_trip(contour) == contour
