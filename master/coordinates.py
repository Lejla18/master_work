from Project1.project1 import get_simple_polygon
from structures.Point import point
from typing import List, Tuple
import turtle

from structures.Polygon import Polygon


def read_file_into_list(filename)->List:
    f = open(filename+'.pol', 'r')
    file = f.read().replace(' ', '\n').replace('/', '\n')
    f.close()
    x = open(filename+'.txt', 'w')

    x.write(file)
    x.close()
    lineList = [int(line.rstrip('\n')) for line in open(filename+'.txt')]
    return lineList


def create_coordinates(filename)->List[point]:

    l = read_file_into_list(filename)

    points = []
    #print(l)

    l_for_extrems = []

    fizicke = []

    for i in range(0, len(l)-3, 4):
        x = (l[i]/l[i+1])
        y = (l[i+2]/l[i+3])

        point_p = point(x, y)

        l_for_extrems.append(x)
        l_for_extrems.append(y)
        points.append(point_p)

    x_coords = []

    for i in range(0, len(l_for_extrems), 2):
        x_coords.append(l_for_extrems[i])

    x_min = min(x_coords)

    print('xmin', x_min)

    for i in range(0, len(l_for_extrems), 2):
        x_coords.append(l_for_extrems[i])

    x_max = max(x_coords)

    print('xmax', x_max)

    y_coords = []

    for i in range(1, len(l_for_extrems), 2):
        y_coords.append(l_for_extrems[i])

    y_min = min(y_coords)

    print('ymin', y_min)

    for i in range(1, len(l_for_extrems), 2):
        y_coords.append(l_for_extrems[i])

    y_max = max(y_coords)

    print('ymax', y_max)

    for item in points:
        x_fiz = turtle.Screen().canvwidth - 0 - (turtle.Screen().canvwidth)*(item.x - x_min)/(x_max-x_min)*2
        y_fiz = turtle.Screen().canvheight - 0 - (turtle.Screen().canvheight)*(item.y - y_min)/(y_max-y_min)*2
        fiz_point = point(x_fiz, y_fiz)
        fizicke.append(fiz_point)


    return fizicke




def return_extrems(filename)->List:

    l = create_coordinates(filename) #fizicke koordinate

    list_of_extrems = []

    x_coords = []
    y_coords = []

    for i in range(0, len(l)):

        x_coords.append(l[i].x)
        y_coords.append(l[i].y)

    x_min = min(x_coords)

    print('xmin', x_min)

    x_max = max(x_coords)

    print('xmax', x_max)

    y_min = min(y_coords)

    print('ymin', y_min)

    y_max = max(y_coords)

    print('ymax', y_max)

    list_of_extrems.append(x_min)
    list_of_extrems.append(x_max)
    list_of_extrems.append(y_min)
    list_of_extrems.append(y_max)

    return list_of_extrems


#p = create_coordinates('randsimple-20-25')
#
# for i in range(0, len(p)):
#     print(p[i])
#
# l = return_extrems('randsimple-20-25')
# print(l)

# def covert_coordinates_of_point(point:point)->point:

#
# #
# p = create_coordinates('randsimple-20-25')
#
# poly = Polygon(get_simple_polygon(p))
#
#
# for point in p:
#     print(point)
#
# poly.draw()
# turtle.done()




