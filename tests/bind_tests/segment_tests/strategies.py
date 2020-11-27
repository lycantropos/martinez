from hypothesis import strategies

from tests.bind_tests.hints import (BoundPoint,
                                    BoundSegment)
from tests.strategies import floats

points = strategies.builds(BoundPoint, floats, floats)
segments = strategies.builds(BoundSegment, points, points)
