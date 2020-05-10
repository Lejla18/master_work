from structures.Point import point
from structures.Polygon import Polygon
from structures.Point import euclid_distance
from structures.Triangle import triangle
from typing import List, Tuple
from structures.Rectangle import rectangle
from cmath import inf
from structures.Stack import Stack
from structures.Segment import segment
import random

#from poly2tri import CDT

# -----------------------------------------------

# orientation of three points

# orientation < 0 - clockwise
# orientation = 0 - colinear
# orientation > 0 - counterclockwise

# -----------------------------------------------


def orientation(p1: point, p2: point, p3: point) -> float:
    product = (p2.x - p1.x) * (p3.y - p1.y) - (p3.x - p1.x) * (p2.y - p1.y)
    if product == 0:
        return 0
    elif product > 0:
        return 1
    else:
        return -1


# -----------------------------------------------

# simple polygon

# -----------------------------------------------
#
def get_x_coordinate(p: point):
    return p.x, p.y


def get_simple_polygon(input_list: List[point]) -> List[point]:
    left_point = sorted(input_list, key=get_x_coordinate)[0]

    # print(left_point)



    def _get_tan(point: point) -> Tuple[float, float]:
        '''
        :param point: upon which calcutes tangens and Euclidean distance
        :return: order of sorting
        '''

        distance = euclid_distance(left_point, point)
        if point.x == left_point.x:
            tan = -inf
        else:
            tan = (point.y - left_point.y) / (point.x - left_point.x)
        if point.y == left_point.y:
            distance *= -1
        return tan, distance

    return sorted(input_list, key=_get_tan)


def get_simple_polygon1(p: Polygon):
    left_point = sorted(p.points, key=get_x_coordinate)[0]

    # print(left_point)

    def _get_tan(point: point) -> Tuple[float, float]:
        '''
        :param point: upon which calcutes tangens and Euclidean distance
        :return: order of sorting
        '''
        distance = euclid_distance(left_point, point)
        if point.x == left_point.x:
            tan = -inf
        else:
            tan = (point.y - left_point.y) / (point.x - left_point.x)
        if point.y == left_point.y:
            distance *= -1
        return tan, distance

    p.points = sorted(p.points, key=_get_tan)


# --------------------------------------------------------------------

# function for checking position of point in relation to triangle

# --------------------------------------------------------------------


def PointInTriangle(p: point, t: triangle) -> bool:
    orientation1 = orientation(t.first, t.second, p)
    # print(orientation1)
    orientation2 = orientation(t.second, t.third, p)
    # print(orientation2)
    orientation3 = orientation(t.third, t.first, p)
    # print(orientation3)

    if (((orientation1 >= 0) and (orientation3 >= 0) and (orientation2 >= 0)) or (
            (orientation1 <= 0) and (orientation3 <= 0) and (orientation2 <= 0))):
        return True
    return False


# --------------------------------------------------------------------

# function for checking position of list of point in relation to triangle


# --------------------------------------------------------------------


def PointsInTriangle(t: triangle, input_list: List[point]) -> List[point]:
    # returns list of point in triangle

    l = list()
    for i in range(0, len(input_list)):
        if (PointInTriangle(input_list[i], t)):
            l.append(input_list[i])
    return l


# -----------------------------------------------

# function for checking convex rectangle

# -----------------------------------------------


def ConvexRectangle(r: rectangle) -> bool:
    orientation1 = orientation(r.first, r.second, r.third)
    orientation2 = orientation(r.second, r.third, r.fourth)
    orientation3 = orientation(r.third, r.fourth, r.first)
    orientation4 = orientation(r.fourth, r.first, r.second)
    #
    # print(orientation1)
    # print(orientation2)
    # print(orientation3)
    # print(orientation4)

    # for convex rectangle every 3 point must have the same orientation
    if (((orientation1 >= 0) and (orientation3 >= 0) and (orientation2 >= 0) and (orientation4 >= 0)) or (
            (orientation1 <= 0) and (orientation3 <= 0) and (orientation2 <= 0) and (orientation4 <= 0))):
        return True
    else:
        return False


# -----------------------------------------------

# intersection of two segments

#  -----------------------------------------------

# when three points are colinear check is point p3 on segment p1p2


def onSegment(p1: point, p2: point, p3: point) -> bool:

    if p3.x <= max(p1.x, p2.x) and p3.x >= min(p1.x, p2.x) and p3.y <= max(p1.y, p2.y) and p3.y >= min(p1.y, p2.y):
        return True
    else:
        return False
def onSegment_real(p1: point, p2: point, p3: point) -> bool:

    if p3.x < max(p1.x, p2.x) and p3.x > min(p1.x, p2.x) and p3.y < max(p1.y, p2.y) and p3.y > min(p1.y, p2.y):
        return True
    else:
        return False

def intersection(s1: segment, s2: segment):
    # return true if segments are intersected

    orientation1 = orientation(s1.first, s1.second, s2.first)
    orientation2 = orientation(s1.first, s1.second, s2.second)
    orientation3 = orientation(s2.first, s2.second, s1.first)
    orientation4 = orientation(s2.first, s2.second, s1.second)

    # general case, different orientation
    if orientation2 != orientation1 and orientation3 != orientation4:
        return True
    # two points colinear and third is on segment of first two
    if orientation1 == 0 and onSegment(s1.first, s1.second, s2.first):
        return True
    if orientation2 == 0 and onSegment(s1.first, s1.second, s2.second):
        return True
    if orientation3 == 0 and onSegment(s2.first, s2.second, s1.first):
        return True
    if orientation4 == 0 and onSegment(s2.first, s2.second, s1.second):
        return True
    return False

def same_segments(s1: segment, s2: segment)->bool:

    if s1.first == s2.first and s1.second == s2.second:
        return True
    if s1.first == s2.second and s1.second == s2.first:
        return True
    return False


def real_intersection(s1: segment, s2: segment):
    # return true if segments are intersected

    orientation1 = orientation(s1.first, s1.second, s2.first)
    orientation2 = orientation(s1.first, s1.second, s2.second)
    orientation3 = orientation(s2.first, s2.second, s1.first)
    orientation4 = orientation(s2.first, s2.second, s1.second)

    # general case, different orientation
    if orientation2 != orientation1 and orientation3 != orientation4 and orientation1 != 0 and orientation2 !=0 and orientation3!=0 and orientation4!=0:
        #print('real intersect')
        return True
    # two points colinear and third is on segment of first two
    if orientation1 == 0 and onSegment_real(s1.first, s1.second, s2.first):
        #print('colinear')
        return True
    if orientation2 == 0 and onSegment_real(s1.first, s1.second, s2.second):
        #print('colinear')

        return True
    if orientation3 == 0 and onSegment_real(s2.first, s2.second, s1.first):
        #print('colinear')

        return True
    if orientation4 == 0 and onSegment_real(s2.first, s2.second, s1.second):
        #print('colinear')

        return True


    return False


def real_intersection_with_same_segments(s1: segment, s2: segment):
    # return true if segments are intersected

    orientation1 = orientation(s1.first, s1.second, s2.first)
    orientation2 = orientation(s1.first, s1.second, s2.second)
    orientation3 = orientation(s2.first, s2.second, s1.first)
    orientation4 = orientation(s2.first, s2.second, s1.second)

    # general case, different orientation
    if orientation2 != orientation1 and orientation3 != orientation4 and orientation1 != 0 and orientation2 != 0 and orientation3 != 0 and orientation4 != 0:
        print('real intersect')
        return True
    # two points colinear and third is on segment of first two
    if orientation1 == 0 and onSegment_real(s1.first, s1.second, s2.first):
        print('colinear')
        return True
    if orientation2 == 0 and onSegment_real(s1.first, s1.second, s2.second):
        print('colinear')

        return True
    if orientation3 == 0 and onSegment_real(s2.first, s2.second, s1.first):
        print('colinear')

        return True
    if orientation4 == 0 and onSegment_real(s2.first, s2.second, s1.second):
        print('colinear')

        return True

    if s1.first == s2.first and s1.second == s2.second:
        return True
    if s1.first == s2.second and s1.second == s2.first:
        return True

    return False


# ---------------------------------------------------------------

# function for checking intersection of segment and polygon

# ---------------------------------------------------------------

def IntersectionP(p: Polygon, s: segment) -> bool:
    i = 0
    counter = 0
    length = len(p.points)
    while i < length:
        s1 = segment(p.points[i], p.points[(i + 1) % length])

        if intersection(s1, s):
            counter = counter + 1
        i += 1
    # print(counter) check how many times segment intersect with polygon
    if counter > 0:
        return True
    else:
        return False

def IntersectionP1(p: Polygon, s: segment) -> bool:
    i = 0
    counter = 0
    length = len(p.points)
    while i < length:
        s1 = segment(p.points[i], p.points[(i + 1) % length])

        if real_intersection(s1, s):
            #counter = counter + 1
            return True
        i += 1
    # print(counter) check how many times segment intersect with polygon

    return False




# -------------------------------------------------

# function for checking orientation of polygon

# --------------------------------------------------

def OrientationOfPolygon(p: Polygon) -> float:
    l = p.points
    # print(l)
    area = 0
    for i in range(0, len(l) - 1):
        area += (l[i + 1].x - l[i].x) * (l[i + 1].y + l[i].y);
    # print(area)
    if area > 0:
        return 1
    else:
        return -1


# -----------------------------------------------------------------

# function for checking position of point in relation to polygon
# Ray - Casting algorithm

# -----------------------------------------------------------------

def PointInsidePolygon(p: point, poly: Polygon):

    extremePoint = point(inf, p.y)
    s = segment(p, extremePoint)

    i = 0  # number of intersections of extreme point and sides od Polygon
    counter = 0
    length = len(poly.points)

    while i < length:
        s1 = segment(poly.points[i], poly.points[(i + 1) % length])

        if intersection(s, s1):

            counter = counter + 1
            if orientation(poly.points[i], p, poly.points[(i + 1) % length]) == 0:
                # print('collinear')
                return False
                    #onSegment(poly.points[i], poly.points[(i + 1) % length], p)
        i += 1
    # print(counter)
    if counter % 2 == 0:
        return False
    else:
        return True


# -----------------------------------------

# function for checking is point on polygon

#--------------------------------------------

def point_on_polygon(p:point, poly:Polygon) -> bool:
    length = len(poly.points)

    for i in range(0, len(poly.points)):
        if orientation(poly.points[i], p, poly.points[(i+1)%length]) == 0:
            return True
    return False
# ------------------------------------------------------------------------

# function for cheking position of list of points in relation to polygon

# -------------------------------------------------------------------------

# this function returns true if polygon p is empty


def emptyPolygon(p: Polygon, input_list: List[point]) -> bool:
    counter = 0

    for i in range(0, len(input_list)):
        if PointInsidePolygon(input_list[i], p):
            counter += 1
    if counter == 0:
        return True
    else:
        return False


# ------------------------------------------------

# Graham scan algorithm for finding convex polygon

# -----------------------------------------------


def graham_scan(input_list: List[point]) -> Polygon:
    # phase1 - sorting points

    input_list1 = get_simple_polygon(input_list)

    # phase2 - creating list of points who generate convex polygon

    s = Stack()

    s.push(input_list1[0])
    s.push(input_list1[1])
    s.push(input_list1[2])

    for i in range(3, len(input_list)):

        while orientation(s.next_to_top(), s.peek(), input_list1[i]) < 0:
            s.pop()
            # print(s.next_to_top(), s.peek(), input_list1[i])

        s.push(input_list1[i])

    l = []

    while not s.is_empty():
        l.append(s.peek())
        s.pop()
    return Polygon(l)


s = segment(point(0, 0), point(5, 5))

s1 = segment(point(5, 5), point(5, 10))

# print(intersection(s, s1))



#-----------------------------------

# generate polygon

#---------------------------------------


def generate_polygon() -> Polygon:

    n = random.randint(3, 20)

    i = 0
    l = []
    while i < n:
        x = random.randint(-300, 300)
        y = random.randint(-300, 300)
        l.append(point(x, y))
        i += 1
    return Polygon(get_simple_polygon(l))