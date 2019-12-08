from _martinez import (Point,
                       Segment)
from hypothesis import strategies

from tests.strategies import single_precision_floats as floats

points = strategies.builds(Point, floats, floats)
segments = strategies.builds(Segment, points, points)
