from structures.Point import point
from structures.Segment import segment
from typing import List, Tuple


class triangle:
    def __init__(self, first: point, second: point, third:point):
        self.first = first
        self.second = second
        self.third=third

    def __eq__(self, other):
        return self.first == other.first and self.second == other.second and self.third == other.third

    # def get_sides(self) -> List[segment]:
    #     return [segment(self.first, self.second), segment(self.second, self.third), segment(self.third, self.first)]

    def get_sides(self) -> List[segment]:
        return [segment(self.first, self.second),
                segment(self.second, self.third),
                segment(self.third, self.first)]

    def draw(self):
        self.first.draw()
        self.second.draw(True)
        self.third.draw(True)
        self.first.draw(True)

    def get_points(self) -> List[point]:

        return [self.first, self.second, self.third]


    def drawSec(self, canvas):
        segments = self.get_sides()
        for segment in segments:
            segment.drawSec(canvas)