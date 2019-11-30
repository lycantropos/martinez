from hypothesis import strategies

from martinez.point import Point
from tests.strategies import scalars

points = strategies.builds(Point, scalars, scalars)
non_points = strategies.builds(object)
