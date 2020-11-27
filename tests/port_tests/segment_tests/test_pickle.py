from hypothesis import given

from tests.port_tests.hints import PortedSegment
from tests.utils import pickle_round_trip
from . import strategies


@given(strategies.segments)
def test_round_trip(segment: PortedSegment) -> None:
    assert pickle_round_trip(segment) == segment
