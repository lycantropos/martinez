import copy

from _martinez import Segment
from hypothesis import given

from . import strategies


@given(strategies.segments)
def test_shallow(segment: Segment) -> None:
    result = copy.copy(segment)

    assert result is not segment
    assert result == segment


@given(strategies.segments)
def test_deep(segment: Segment) -> None:
    result = copy.deepcopy(segment)

    assert result is not segment
    assert result == segment
