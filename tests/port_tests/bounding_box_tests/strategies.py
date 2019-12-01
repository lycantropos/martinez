from typing import Tuple

from hypothesis import strategies

from martinez.bounding_box import BoundingBox
from martinez.hints import Scalar
from tests.strategies import scalars_strategies
from tests.utils import Strategy


def scalars_to_quadruples(scalars: Strategy[Scalar]
                          ) -> Strategy[Tuple[Scalar, Scalar, Scalar, Scalar]]:
    return strategies.tuples(scalars, scalars, scalars, scalars)


scalars_quadruples = scalars_strategies.flatmap(scalars_to_quadruples)


def scalars_to_bounding_boxes(scalars: Strategy[Scalar]
                              ) -> Strategy[BoundingBox]:
    return strategies.builds(BoundingBox, scalars, scalars, scalars, scalars)


bounding_boxes = scalars_strategies.flatmap(scalars_to_bounding_boxes)
non_bounding_boxes = strategies.builds(object)
