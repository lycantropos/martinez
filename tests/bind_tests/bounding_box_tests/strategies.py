from hypothesis import strategies

from tests.bind_tests.hints import BoundBoundingBox as BoundingBox
from tests.strategies import floats

floats = floats
bounding_boxes = strategies.builds(BoundingBox, floats, floats, floats, floats)
