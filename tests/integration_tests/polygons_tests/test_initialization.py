from typing import (List,
                    Tuple)

from hypothesis import given

from tests.bind_tests.hints import (BoundContour,
                                    BoundPolygon)
from tests.integration_tests.utils import are_bound_ported_polygons_equal
from tests.port_tests.hints import (PortedContour,
                                    PortedPolygon)
from . import strategies


@given(strategies.contours_lists_pairs)
def test_basic(contours_lists_pair: Tuple[List[BoundContour],
                                          List[PortedContour]]) -> None:
    bound_contours, ported_contours = contours_lists_pair

    bound, ported = (BoundPolygon(bound_contours),
                     PortedPolygon(ported_contours))

    assert are_bound_ported_polygons_equal(bound, ported)
