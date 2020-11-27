from hypothesis import given

from tests.port_tests.hints import PortedSegment
from . import strategies


@given(strategies.segments)
def test_basic(segment: PortedSegment) -> None:
    assert isinstance(segment.reversed, PortedSegment)


@given(strategies.segments)
def test_involution(segment: PortedSegment) -> None:
    assert segment.reversed.reversed == segment
