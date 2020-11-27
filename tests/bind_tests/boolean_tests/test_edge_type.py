from tests.bind_tests.hints import BoundEdgeType

from tests.utils import all_unique


def test_basic():
    assert all_unique(BoundEdgeType.__members__.values())
