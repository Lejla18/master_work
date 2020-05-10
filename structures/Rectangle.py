from structures.Point import point
import turtle

class rectangle:
    def __init__(self, first: point, second: point, third:point, fourth:point):
        self.first = first
        self.second = second
        self.third=third
        self.fourth = fourth

    def __eq__(self, other):
        return ((self.first == other.first) and (self.second == other.second) and (self.third==other.third) and (self.fourth==other.fourth))

    def draw(self):
        self.first.draw()
        self.second.draw(True)
        self.third.draw(True)
        self.fourth.draw(True)
        self.first.draw(True)


