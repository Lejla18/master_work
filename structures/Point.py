
'class point in two dimensions'

import math
from collections import namedtuple
import turtle
from tkinter import Canvas
from structures.conf import CENTER

turtle = turtle.Turtle()


class point(namedtuple('point', ['x', 'y'])):

    def draw(self, forbbid_drop=False):

        if not forbbid_drop:
            turtle.up()
        turtle.setpos(self.x, self.y)
        turtle.down()
        turtle.dot()

    def udaljenost(self, p):
        dx = self.x - p.x
        dy = self.y - p.y
        return math.sqrt(dx ** 2 + dy ** 2)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def daj_x(self):
        return self.x

    def drawSec(self, canvas: Canvas) -> None:
        """
        Draws point on to the canvas. Takes translation into consideration.

        Args:
            canvas: Canvas object on which line segment will be drawn to.
        """
        x = self.x + CENTER
        y = -(self.y - CENTER)

        canvas.create_oval(x - 2, y - 2, x + 2, y + 2, width=0, fill="blue")

    def drawGuard(self, canvas: Canvas) -> None:
            """
            Draws point on to the canvas. Takes translation into consideration.

            Args:
                canvas: Canvas object on which line segment will be drawn to.
            """
            x = self.x + CENTER
            y = -(self.y - CENTER)

            canvas.create_oval(x - 2, y - 2, x + 2, y + 2, width=0, fill="red")

    def drawReflex(self, canvas: Canvas) -> None:
        """
        Draws point on to the canvas. Takes translation into consideration.

        Args:
            canvas: Canvas object on which line segment will be drawn to.
        """
        x = self.x + CENTER
        y = -(self.y - CENTER)

        canvas.create_oval(x - 2, y - 2, x + 2, y + 2, width=3, fill="black")

# p1 = point(3,5)
# p1.draw()
# turtle.done()


def euclid_distance(p1: point, p2: point) -> float:
    return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)


