from hypothesis import given

from tests.port_tests.hints import PortedPoint
from tests.utils import pickle_round_trip
from . import strategies


@given(strategies.points)
def test_round_trip(point: PortedPoint) -> None:
    assert pickle_round_trip(point) == point
