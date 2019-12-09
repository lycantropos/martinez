from _martinez import OperationType

from tests.utils import all_unique


def test_basic():
    assert all_unique(OperationType.__members__.values())
