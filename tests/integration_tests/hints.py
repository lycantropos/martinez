from typing import Tuple

from tests.bind_tests.hints import (BoundPoint,
                                    BoundSweepEvent)
from tests.port_tests.hints import (PortedPoint,
                                    PortedSweepEvent)

BoundPortedPointsPair = Tuple[BoundPoint, PortedPoint]
BoundPortedSweepEventsPair = Tuple[BoundSweepEvent, PortedSweepEvent]
