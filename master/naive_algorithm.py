import random, time, turtle

from master.coordinates import create_coordinates, return_extrems
from structures.Polygon import Polygon
from structures.Segment import segment
from typing import List
from Project1.project1 import get_simple_polygon, PointInsidePolygon, IntersectionP1, same_segments
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

    polygon = Polygon(input_list)

    polygon_vertices = input_list

    while len(visible_vertex) < len(polygon_vertices):

        print("novi while")
        random_guard = generate_point_inside_polygon(filename, polygon)
        print("izabrao random tacku")

        for vertex in polygon_vertices:
            print("vertex", vertex)

            if vertex not in visible_vertex:
                s = segment(random_guard, vertex)
                p1 = point((vertex.x + random_guard.x)/2, (vertex.y+random_guard.y)/2)

                if not IntersectionP1(polygon, s) and PointInsidePolygon(p1, polygon):
                    visible_vertex.append(vertex)
                    if random_guard not in guards:
                        guards.append(random_guard)
                        print("dosao do guarda")

                    # slucaj kada se segmenti preklapaju, tj kada cuvar sa refleksne ivice vidi susjedni vrh
                else:
                    for i in range(0, len(polygon.points)):
                        seg = segment(polygon.points[i], polygon.points[(i + 1) % len(polygon.points)])
                        if same_segments(seg, s):
                            visible_vertex.append(vertex)

    return guards



def try_n_times(n: int, filename)->List[point]:

    start_time = time.time()

    min = 100
    max = 0
    srednja = 0
    final_guards = []
    for i in range(0, n):
        guards = run_naive_algorithm(filename)
        if min > len(guards):
            min = len(guards)
            final_guards = guards
        if max < len(guards):
            max = len(guards)

        srednja = srednja + len(guards)
    print('max', max)
    print('srednja', srednja/n)
    print('min', min)
    print('final guards', final_guards)

    print("--- %s seconds ---" % (time.time() - start_time))

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






#print('rs-80-1', try_n_times(30, 'randsimple-80-1'))
#print('rs-80-2', try_n_times(30, 'randsimple-80-2'))
#print('rs-80-3', try_n_times(30, 'randsimple-80-3'))
#print('rs-80-4', try_n_times(30, 'randsimple-80-4'))
#print('rs-80-5', try_n_times(30, 'randsimple-80-5'))
#print('rs-80-6', try_n_times(30, 'randsimple-80-6'))
#print('rs-80-7', try_n_times(30, 'randsimple-80-7'))
# print('rs-80-8', try_n_times(30, 'randsimple-80-8'))
# print('rs-80-9', try_n_times(30, 'randsimple-80-9'))
# print('rs-80-10', try_n_times(30, 'randsimple-80-10'))
# print('rs-80-11', try_n_times(30, 'randsimple-80-11'))
# print('rs-80-12', try_n_times(30, 'randsimple-80-12'))
# print('rs-80-13', try_n_times(30, 'randsimple-80-13'))
# print('rs-80-14', try_n_times(30, 'randsimple-80-14'))
# print('rs-80-15', try_n_times(30, 'randsimple-80-15'))
# print('rs-80-16', try_n_times(30, 'randsimple-80-16'))
# print('rs-80-17', try_n_times(30, 'randsimple-80-17'))
# print('rs-80-18', try_n_times(30, 'randsimple-80-18'))
# print('rs-80-19', try_n_times(30, 'randsimple-80-19'))
# print('rs-80-20', try_n_times(30, 'randsimple-80-20'))
# print('rs-80-21', try_n_times(30, 'randsimple-80-21'))
# print('rs-80-22', try_n_times(30, 'randsimple-80-22'))
# print('rs-80-23', try_n_times(30, 'randsimple-80-23'))
# print('rs-80-24', try_n_times(30, 'randsimple-80-24'))
# print('rs-80-25', try_n_times(30, 'randsimple-80-25'))
# print('rs-80-26', try_n_times(30, 'randsimple-80-26'))
# print('rs-80-27', try_n_times(30, 'randsimple-80-27'))
# print('rs-80-28', try_n_times(30, 'randsimple-80-28'))
# print('rs-80-29', try_n_times(30, 'randsimple-80-29'))
# print('rs-80-30', try_n_times(30, 'randsimple-80-30'))





























