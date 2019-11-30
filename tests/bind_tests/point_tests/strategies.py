from _martinez import Point_2
from hypothesis import strategies

from tests.strategies import floats

points = strategies.builds(Point_2, floats, floats)
