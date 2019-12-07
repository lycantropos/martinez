from .point import Point


def sign(first_point: Point, second_point: Point, third_point: Point) -> int:
    determinant = ((first_point.x - third_point.x)
                   * (second_point.y - third_point.y)
                   - (second_point.x - third_point.x)
                   * (first_point.y - third_point.y))
    if determinant > 0:
        return 1
    elif determinant < 0:
        return -1
    else:
        return 0
