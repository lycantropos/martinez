from hypothesis import strategies

from tests.bind_tests.hints import BoundPoint
from tests.strategies import floats

points = strategies.builds(BoundPoint, floats, floats)
