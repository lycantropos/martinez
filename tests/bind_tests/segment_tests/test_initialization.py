from hypothesis import given

from tests.bind_tests.hints import (BoundPoint,
                                    BoundSegment)
from . import strategies


@given(strategies.points, strategies.points)
def test_basic(source: BoundPoint, target: BoundPoint) -> None:
    result = BoundSegment(source, target)

    assert result.source == source
    assert result.target == target
