from master.coordinates import create_coordinates, return_extrems
from structures.Polygon import Polygon
from structures.Segment import segment
from typing import List
from Project1.project1 import get_simple_polygon, PointInsidePolygon, IntersectionP1
import random
from structures.Point import point


def generate_point_inside_polygon(filename, poly:Polygon)->point:

    l = return_extrems(filename)

    p = point(random.randint(l[0], l[1]), random.randint(l[2], l[3]))
    while not PointInsidePolygon(p, poly):
        p = point(random.randint(l[0], l[1]), random.randint(l[2], l[3]))
    print('generated point', p)
    return p



# def run_naive_algorithm(input_list: List[point])-> List[point]:
#
#     polygon = Polygon(get_simple_polygon(input_list))
#
#     guards = []
#     visible_vertex = []
#
#     polygon_vertices = get_simple_polygon(input_list)
#
#     while len(visible_vertex) != len(get_simple_polygon(input_list)):
#
#         random_guard = generate_point_inside_polygon(polygon)
#
#         for vertex in polygon_vertices:
#
#             s = segment(random_guard, vertex)
#
#             if not IntersectionP(polygon, s):
#
#                 guards.append(vertex)
#                 print(vertex)
#
#             visible_vertex.append(vertex)
#
#         for vertex in visible_vertex:
#             polygon_vertices.remove(vertex)
#
#     return guards

def run_naive_algorithm(filename)-> List[point]:

    input_list = create_coordinates(filename)
    guards = []
    visible_vertex = []

    polygon = Polygon(get_simple_polygon(input_list))

    polygon_vertices = get_simple_polygon(input_list)

    while len(visible_vertex) < len(polygon_vertices):

        print("novi while")
        random_guard = generate_point_inside_polygon(filename, polygon)
        print("izabrao random tacku")

        for vertex in polygon_vertices:
            print("vertex", vertex)

            if vertex not in visible_vertex:
                s = segment(random_guard, vertex)

                if not IntersectionP1(polygon, s):

                    print("provjerio za jedan vertex")
                    visible_vertex.append(vertex)
                    if random_guard not in guards:
                        guards.append(random_guard)
                        print("dosao do guarda")

    return guards



def try_n_times(n: int, filename)->List[point]:
    min = 100
    final_guards = []
    for i in range(0, n):
        guards = run_naive_algorithm(filename)
        if min > len(guards):
            min = len(guards)
            final_guards = guards

    print(min)
    print('final guards', final_guards)
    return final_guards




# guards = try_100_times()
#
#
# p = create_coordinates('randsimple-20-25')
# poly = Polygon(get_simple_polygon(p))
#
# for guard in guards:
#     guard.draw()
# poly.draw()
# turtle.done()

# #
# # for point in p:
# #     print(point)
# #
# #
# guards = run_naive_algorithm('randsimple-20-17')
#
#
# for guard in guards:
#     print("guard", guard)
# print('broj cuvara ', len(guards))
#
#











