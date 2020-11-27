from hypothesis import given

from tests.port_tests.hints import (PortedPoint,
                                    PortedSegment)
from . import strategies


@given(strategies.segments)
def test_basic(segment: PortedSegment) -> None:
    result = segment.min

    assert isinstance(result, PortedPoint)
    assert result == segment.source or result == segment.target
