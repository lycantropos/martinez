from _martinez import (Point,
                       Segment)
from hypothesis import strategies

from tests.strategies import floats

points = strategies.builds(Point, floats, floats)
segments = strategies.builds(Segment, points, points)
