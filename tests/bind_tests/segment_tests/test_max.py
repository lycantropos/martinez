from hypothesis import given

from tests.bind_tests.hints import (BoundPoint,
                                    BoundSegment)
from . import strategies


@given(strategies.segments)
def test_basic(segment: BoundSegment) -> None:
    result = segment.max

    assert isinstance(result, BoundPoint)
    assert result == segment.source or result == segment.target
