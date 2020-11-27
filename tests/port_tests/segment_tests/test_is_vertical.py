from hypothesis import given

from tests.port_tests.hints import PortedSegment
from . import strategies


@given(strategies.segments)
def test_basic(segment: PortedSegment) -> None:
    result = segment.is_vertical

    assert isinstance(result, bool)
