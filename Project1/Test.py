from Project1.project1 import get_simple_polygon

from master.coordinates import create_coordinates
from master.triangulation import ear_clipping
from structures.Polygon import Polygon
import turtle

# ---------------------------------

# test for orientation of three points

# ---------------------------------

# p1 = point(random.randint(-300,300), random.randint(-300,300))
# p2 = point(random.randint(-300,300), random.randint(-300,300))
# p3 = point(random.randint(-300,300), random.randint(-300,300))
#
# p1.draw()
# p2.draw()
# p3.draw()
#
# result = orientation(p1,p2,p3)
#
# if result < 0 :
#     print ('Clockwise')
# if result > 0 :
#     print ('Counterclockwise')
# if result == 0 :
#     print('Colinear')
#
# # # print(result)
# #
# turtle.done()





# ---------------------------

# test for simple polygon

# --------------------------

# n = random.randint(3, 6)
#
# i = 0
# l = []
# while i < n:
#     x = random.randint(-300, 300)
#     y = random.randint(-300, 300)
#     l.append(point(x, y))
#     i += 1
#
# print("Number of points :", n)
# print("Points :")
# for i in range(0, len(l)):
#     print(l[i])
#
# p = Polygon(get_simple_polygon(l))
#
#
# p.draw()
# turtle.done()



# ------------------------------------

# test for function PointInTriangle

# -----------------------------------
#
# i = 0
# l = []
# while i < 3 :
#     x = random.randint(-300, 300)
#     y = random.randint(-300,300)
#     l.append(point(x,y))
#     i += 1
#
# print ("Points of triangle :")
# for i in range(0, len(l)):
#     print(l[i])
#
# p = point(random.randint(-300,300), random.randint(-300,300))
#
# print ("Point p: ", p)
#
# t=triangle(l[0],l[1],l[2])
#
#
# if (PointInTriangle(p, t) == True):
#     print('Point is in Triangle')
# else:
#     print('Point is out of range of Triangle')
#
#
#
# p.draw()
# t.draw()
#
# turtle.done()
#


# ------------------------------------

# test for function PointsInTriangle

# -----------------------------------
#
#
#
# i = 0
# l1 = []
# while i < 3 :
#     x = random.randint(-300, 300)
#     y = random.randint(-300,300)
#     l1.append(point(x,y))
#     i += 1
#
# print ("Points of triangle : ")
# for i in range(0, len(l1)):
#     print(l1[i])
#
#
# n = random.randint(0,20)
# k = 0
# points = []
# while i < n :
#     x = random.randint(-300, 300)
#     y = random.randint(-300,300)
#     points.append(point(x,y))
#     i += 1
#
# print("Points in list :")
#
# for i in range(0, len(points)):
#     print(points[i])
#
#
# t=triangle(l1[0],l1[1],l1[2])
#
#
# print('points in triangle :')
# print(PointsInTriangle(t, points))
#
#
# for point in points:
#     point.draw()
#
# t.draw()
#
# turtle.done()



# ------------------------------------

# test for function ConvexRectangle

# -----------------------------------

#
# i = 0
# l = []
# while i < 4 :
#     x = random.randint(-200, 200)
#     y = random.randint(-200,200)
#     l.append(point(x,y))
#     i += 1
#
# for i in range(0, len(l)):
#     print(l[i])
#
#
# t=rectangle(l[0],l[1],l[2],l[3])
#
#
# if (ConvexRectangle(t) == True):
#     print('Rectangle is convex')
# else:
#     print('Rectangle is not convex')
#
# t.draw()
# turtle.done()
#


# ------------------------------------

# test for intersection of two segments

# -----------------------------------

#
# p1 = point(random.randint(-300,300), random.randint(-300,300))
# p2 = point(random.randint(-300,300), random.randint(-300,300))
# p3 = point(random.randint(-300,300), random.randint(-300,300))
# p4 = point(random.randint(-300,300), random.randint(-300,300))
#
#
# s1 = segment(p1,p2)
# s2 = segment(p3,p4)
#
# s1.draw()
# s2.draw()
# if (intersection(s1,s2)):
#     print("Intersect")
# else :
#     print("Do not intersect")
# turtle.done()


# ------------------------------------------

# test for intersection segment and polygon

# ------------------------------------------


#
#
# n = random.randint(3, 20)
#
# i = 0
# l = []
# while i < n:
#     x = random.randint(-300, 300)
#     y = random.randint(-300,300)
#     l.append(point(x,y))
#     i += 1
#
#
# print("Number of points :", n)
# print("Points :")
# for i in range(0, len(l)):
#     print(l[i])
#
# p = Polygon(get_simple_polygon(l))
#
# p1 = point(random.randint(-300,300), random.randint(-300,300))
# p2 = point(random.randint(-300,300), random.randint(-300,300))
#
# s = segment(p1, p2)
# print('segment')
# s.printSegment()
# if (IntersectionP1(p, s)):
#     print("Intersect")
# else : print("Do not intersect")
# s.draw()
# p.draw()
#
# turtle.done()
#


# ------------------------------

# test for orientation of polygon

# ------------------------------


#
# n = random.randint(3, 20)
#
#
# i = 0
# l1 = []
# while i < n :
#     x = random.randint(-300, 300)
#     y = random.randint(-300,300)
#     l1.append(point(x,y))
#     i += 1
#
#
# print("Number of points :", n)
# print("Points :")
# for i in range(0, len(l1)):
#     print(l1[i])
#
#
# p = Polygon(get_simple_polygon(l1))
#
# result = OrientationOfPolygon(p)
#
# if result == 1 :
#     print("Clockwise")
# else :
#     print ("Counter - clockwise")
#
#
# p.draw()
# turtle.done()
#



# ---------------------------------------------------------

# test for checking position of point in relation to polygon

# ------------------------------------------------------------


# n = random.randint(3, 20)
#
#
# i = 0
# l = []
# while i < n:
#     x = random.randint(-300, 300)
#     y = random.randint(-300, 300)
#     l.append(point(x, y))
#     i += 1
#
#
# p1 = point(random.randint(-300, 300), random.randint(-300, 300))
# p = Polygon(get_simple_polygon(l))
#
# if PointInsidePolygon(p1, p):
#     print("Point is in the polygon")
# else:
#     print("Point is out of the polygon")
#
#
#
# p1.draw()
# p.draw()
#
# turtle.done()

# ---------------------------------------------------------

# test for checking empty polygon

# ------------------------------------------------------------
#
# f = random.randint(2,20)
# k = 0
# points = []
# while k < f :
#     x = random.randint(-300, 300)
#     y = random.randint(-300,300)
#     points.append(point(x,y))
#     k += 1
#
# print("Points in list :")
#
# for i in range(0, len(points)):
#     print(points[i])
#
#
# n = random.randint(3, 20)
#
#
# i = 0
# l = []
# while i < n :
#     x = random.randint(-300, 300)
#     y = random.randint(-300,300)
#     l.append(point(x,y))
#     i += 1
#
# p = Polygon(get_simple_polygon(l))
#
#
# if(emptyPolygon(p, points)):
#     print("Polygon is empty")
# else :
#     print ("Polygon is not empty")
#
#
# for point in points:
#     point.draw()
#
# p.draw()
#
#
# turtle.done()


# ------------------------------------------

# test for Graham scan algorithm

# ------------------------------------------

#
# n = random.randint(4, 20)
# print(n)
#
# i = 0
# l1 = []
# while i < n :
#     x = random.randint(-300, 300)
#     y = random.randint(-300,300)
#     l1.append(point(x,y))
#     print(l1[i])
#     i += 1
#
#
#
# p = graham_scan(l1)
#
# p.draw()
#
# turtle.done()


# -----------------------------------------------

# test for run_naive_algorithm

# ----------------------------------------------


# n = random.randint(3, 6)
#
# i = 0
# l = []
# while i < n:
#     x = random.randint(-300, 300)
#     y = random.randint(-300, 300)
#     l.append(point(x, y))
#     print(point(x, y))
#     i += 1
#
# p = Polygon(get_simple_polygon(l))
# print(l)
#
# guards = run_naive_algorithm(l)
#
# for guard in guards:
#     print("guard", guard)


#--------------------------------

#test for real intersection of two segments

#----------------------------------




# p1 = point(random.randint(-300,300), random.randint(-300,300))
# p2 = point(random.randint(-300,300), random.randint(-300,300))
# p3 = point(random.randint(-300,300), random.randint(-300,300))
# p4 = point(random.randint(-300,300), random.randint(-300,300))
#
#
# p5 = point(50, 50)
# p6 = point(100, 100)
# p7 = point(50, 50)
# p8 = point(0, 60)
# # s1 = segment(p1, p2)
# # s2 = segment(p3, p4)
# #
# s1 = segment(p5, p6)
# s2 = segment(p7, p8)
#
# s1.draw()
# s2.draw()
# if real_intersection(s1, s2):
#     print("Intersect")
# else:
#     print("Do not intersect")
#
#
# turtle.done()

#
#
# n = random.randint(3, 10)
#
#
# i = 0
# l = []
# while i < n:
#     x = random.randint(-300, 300)
#     y = random.randint(-300, 300)
#     l.append(point(x, y))
#     i += 1
#
#
# p1 = point(random.randint(-300, 300), random.randint(-300, 300))
# p = Polygon(get_simple_polygon(l))
# print(p.convexPolygon())
# p.draw()
# print(p.convexPolygon())


# p = create_coordinates('randsimple-20-25')
# polygon = Polygon(get_simple_polygon(p))
#
# triangles = ear_clipping(polygon)
#
# for t in triangles:
#     t.draw()
#
# turtle.done()