from _martinez import EdgeType

from tests.utils import all_unique


def test_basic():
    assert all_unique(EdgeType.__members__.values())
