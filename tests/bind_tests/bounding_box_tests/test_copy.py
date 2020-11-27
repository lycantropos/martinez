import copy

from hypothesis import given

from tests.bind_tests.hints import BoundBoundingBox
from . import strategies


@given(strategies.bounding_boxes)
def test_shallow(bounding_box: BoundBoundingBox) -> None:
    result = copy.copy(bounding_box)

    assert result is not bounding_box
    assert result == bounding_box


@given(strategies.bounding_boxes)
def test_deep(bounding_box: BoundBoundingBox) -> None:
    result = copy.deepcopy(bounding_box)

    assert result is not bounding_box
    assert result == bounding_box
