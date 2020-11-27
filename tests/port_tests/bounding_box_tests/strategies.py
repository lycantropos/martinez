from typing import Tuple

from hypothesis import strategies

from tests.port_tests.hints import PortedBoundingBox
from tests.strategies import scalars_strategies
from tests.utils import (Scalar,
                         Strategy)


def scalars_to_quadruples(scalars: Strategy[Scalar]
                          ) -> Strategy[Tuple[Scalar, Scalar, Scalar, Scalar]]:
    return strategies.tuples(scalars, scalars, scalars, scalars)


scalars_quadruples = scalars_strategies.flatmap(scalars_to_quadruples)


def scalars_to_bounding_boxes(scalars: Strategy[Scalar]
                              ) -> Strategy[PortedBoundingBox]:
    return strategies.builds(PortedBoundingBox, scalars, scalars, scalars,
                             scalars)


bounding_boxes = scalars_strategies.flatmap(scalars_to_bounding_boxes)
