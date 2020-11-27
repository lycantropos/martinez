from hypothesis import given

from tests.bind_tests.hints import BoundBoundingBox
from . import strategies


@given(strategies.bounding_boxes, strategies.bounding_boxes)
def test_basic(first_bounding_box: BoundBoundingBox,
               second_bounding_box: BoundBoundingBox) -> None:
    result = first_bounding_box + second_bounding_box

    assert isinstance(result, BoundBoundingBox)


@given(strategies.bounding_boxes)
def test_idempotence(bounding_box: BoundBoundingBox) -> None:
    assert bounding_box + bounding_box == bounding_box


@given(strategies.bounding_boxes, strategies.bounding_boxes)
def test_commutativity(first_bounding_box: BoundBoundingBox,
                       second_bounding_box: BoundBoundingBox) -> None:
    assert (first_bounding_box + second_bounding_box
            == second_bounding_box + first_bounding_box)


@given(strategies.bounding_boxes,
       strategies.bounding_boxes,
       strategies.bounding_boxes)
def test_associativity(first_bounding_box: BoundBoundingBox,
                       second_bounding_box: BoundBoundingBox,
                       third_bounding_box: BoundBoundingBox) -> None:
    assert ((first_bounding_box + second_bounding_box) + third_bounding_box
            == first_bounding_box + (second_bounding_box + third_bounding_box))
