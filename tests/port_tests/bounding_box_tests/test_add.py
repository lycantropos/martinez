from hypothesis import given

from martinez.bounding_box import BoundingBox
from . import strategies


@given(strategies.bounding_boxes, strategies.bounding_boxes)
def test_basic(first_bounding_box: BoundingBox,
               second_bounding_box: BoundingBox) -> None:
    result = first_bounding_box + second_bounding_box

    assert isinstance(result, BoundingBox)


@given(strategies.bounding_boxes)
def test_idempotence(bounding_box: BoundingBox) -> None:
    assert bounding_box + bounding_box == bounding_box


@given(strategies.bounding_boxes, strategies.bounding_boxes)
def test_commutativity(first_bounding_box: BoundingBox,
                       second_bounding_box: BoundingBox) -> None:
    assert (first_bounding_box + second_bounding_box
            == second_bounding_box + first_bounding_box)


@given(strategies.bounding_boxes,
       strategies.bounding_boxes,
       strategies.bounding_boxes)
def test_associativity(first_bounding_box: BoundingBox,
                       second_bounding_box: BoundingBox,
                       third_bounding_box: BoundingBox) -> None:
    assert ((first_bounding_box + second_bounding_box) + third_bounding_box
            == first_bounding_box + (second_bounding_box + third_bounding_box))
