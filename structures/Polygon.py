'''
Class Polygon
'''
import turtle
from typing import List
from structures.Point import euclid_distance
from structures.Segment import segment
from structures.Point import point
from structures.Point import euclid_distance
from structures.Triangle import triangle
from typing import List, Tuple
import random

def get_x_coordinate(point: point):

    return point.x, -point.y


def orientation(p1: point, p2: point, p3: point) -> float:
    product = (p2.x - p1.x) * (p3.y - p1.y) - (p3.x - p1.x) * (p2.y - p1.y)
    if product == 0:
        return 0
    elif product > 0:
        return 1
    else:
        return -1

class Polygon:
    def __init__(self, points: List[point]):
        self.points = points

    def make_simple(self) -> None:
        """
        For a given polygon (self), transforms it to simple polygon.
        Starts from left most top most point.
        """

        def get_tan(_point: 'point') -> tuple:
            """
            Calculates tangent value of angle between ref_point and _point.
            Args:
                _point: Point object.

            Returns: Value of tan between ref_point and _point.

            """
            distance = euclid_distance(left_p, _point)

            tan = left_p.slope(_point)

            if left_p.y == _point.y:
                distance *= -1

            return tan, distance

        left_p = sorted(self.points, key=lambda p: (point.x, -point.y))[0]
        self.points = sorted(self.points, key=lambda p: get_tan(p))

    def draw(self):
        i = 0
        length = self.points.__len__()
        while i < length:
            s = segment(self.points[i], self.points[(i+1)%length])
            s.draw()
            i += 1
        turtle.done()

    def GetEdges(self)->list:
        edges = []
        i = 0
        length = self.points.__len__()
        while i < length:
            s = segment(self.points[i], self.points[(i + 1) % length])
            i += 1
        return edges

    def getList(self)->list:

        l = []
        i = 0
        length = self.points.__len__()
        while i < length:
           l[i] = self.points[i];
           i += 1
        return l

    def drawTwo(self, canvas) -> None:
        """
        Draws polygon object onto the canvas.Takes translation into
        consideration.

        Args:
            canvas: Canvas object on which line segment will be drawn to.
        """

        first = self.points[0]

        for i in range(0, len(self.points) - 1):
            segment(self.points[i], self.points[i + 1]).drawSec(canvas)

        segment(self.points[-1], first).drawSec(canvas)

    def convexPolygon(self) -> bool:

        for i in range(0, len(self.points)-1):
            if orientation(self.points[i], self.points[(i+1)], self.points[(i+2) % len(self.points)]) < 0:
                return False

        return True


