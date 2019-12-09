import enum


@enum.unique
class EdgeType(enum.IntEnum):
    NORMAL = 0
    NON_CONTRIBUTING = 1
    SAME_TRANSITION = 2
    DIFFERENT_TRANSITION = 3


@enum.unique
class OperationType(enum.IntEnum):
    INTERSECTION = 0
    UNION = 1
    DIFFERENCE = 2
    XOR = 3
