from hypothesis import strategies

from martinez.bounding_box import BoundingBox
from tests.strategies import floats

floats = floats
bounding_boxes = strategies.builds(BoundingBox, floats, floats, floats, floats)
non_bounding_boxes = strategies.builds(object)
