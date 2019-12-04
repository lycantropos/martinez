import copy

from hypothesis import given

from martinez.bounding_box import BoundingBox
from . import strategies


@given(strategies.bounding_boxes)
def test_shallow(bounding_box: BoundingBox) -> None:
    result = copy.copy(bounding_box)

    assert result is not bounding_box
    assert result == bounding_box


@given(strategies.bounding_boxes)
def test_deep(bounding_box: BoundingBox) -> None:
    result = copy.deepcopy(bounding_box)

    assert result is not bounding_box
    assert result == bounding_box
