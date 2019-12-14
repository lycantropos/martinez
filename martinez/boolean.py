import enum


@enum.unique
class OperationType(enum.IntEnum):
    INTERSECTION = 0
    UNION = 1
    DIFFERENCE = 2
    XOR = 3
