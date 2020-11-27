from hypothesis import strategies

from tests.bind_tests.hints import BoundBoundingBox
from tests.strategies import floats

floats = floats
bounding_boxes = strategies.builds(BoundBoundingBox, floats, floats, floats,
                                   floats)
