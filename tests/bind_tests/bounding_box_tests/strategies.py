from _martinez import BoundingBox
from hypothesis import strategies

from tests.strategies import floats

floats = floats
bounding_boxes = strategies.builds(BoundingBox, floats, floats, floats, floats)
