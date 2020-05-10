from structures.Point import point
import turtle
# from Project1.project1 import orientation
from structures.Point import point
from tkinter import Canvas
from structures.conf import CENTER


def orientation(p1: point, p2: point, p3: point) -> float:
    product = (p2.x-p1.x)*(p3.y-p1.y) - (p3.x-p1.x)*(p2.y-p1.y)
    if product == 0:
        return 0
    elif product > 0:
        return 1
    else:
        return -1


class segment:

    first=None
    second=None

    def __init__(self, first: point, second: point):
        self.first = first
        self.second = second

    def reversed(self) -> 'segment':
        """
        Reverses direction of LineSegment (self) by switching first and
        second point.

        Returns: Reversed line segment.
        """

        return segment(self.second, self.first)

    def is_equal_undirected(self, other: 'segment') -> bool:
        """
        Determines if two LineSegments are the same regardless of their
        direction.

        Args:
            other: Another line segment.

        Returns: True if segments match, False otherwise.
        """

        return self == other or self == other.reversed()

    def __eq__(self, other):
        return (self.first == other.first) and (self.second == other.second)

    def draw(self):
        self.first.draw()
        self.second.draw(True)

    def printSegment(self):
        print(self.first, self.second)

    def drawSec(self, canvas: Canvas) -> None:
        """
        Draws line segment on to the canvas. Takes translation into
        consideration.

        Args:
            canvas: Canvas object on which line segment will be drawn to.
        """

        first_x = self.first.x + CENTER
        first_y = -(self.first.y - CENTER)
        second_x = self.second.x + CENTER
        second_y = -(self.second.y - CENTER)

        canvas.create_line(first_x, first_y, second_x, second_y,
                           width=1, fill="blue")

    def drawSeg(self, canvas: Canvas) -> None:
        """
        Draws line segment on to the canvas. Takes translation into
        consideration.

        Args:
            canvas: Canvas object on which line segment will be drawn to.
        """

        first_x = self.first.x + CENTER
        first_y = -(self.first.y - CENTER)
        second_x = self.second.x + CENTER
        second_y = -(self.second.y - CENTER)

        canvas.create_line(first_x, first_y, second_x, second_y,
                           width=1, fill="red")
