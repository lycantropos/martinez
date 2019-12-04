import copy

from hypothesis import given

from martinez.segment import Segment
from . import strategies


@given(strategies.segments)
def test_shallow(segment: Segment) -> None:
    result = copy.copy(segment)

    assert result is not segment
    assert result == segment
    assert result.source is segment.source
    assert result.target is segment.target


@given(strategies.segments)
def test_deep(segment: Segment) -> None:
    result = copy.deepcopy(segment)

    assert result is not segment
    assert result == segment
    assert result.source is not segment.source
    assert result.target is not segment.target
