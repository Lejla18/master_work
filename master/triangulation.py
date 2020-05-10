from master.coordinates import create_coordinates
from Project1.project1 import *
from structures.Triangle import triangle
from structures.Polygon import Polygon
import random, time, turtle


def is_convex_vertex(pprev: point, pcurr: point, pnext: point) -> bool:
    return orientation(pprev, pcurr, pnext) > 0


def _triangle_area(x1, y1, x2, y2, x3, y3):
    return abs((x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2.0)



def is_ear(prev_vertex, current_vertex, next_vertex, poly: Polygon) -> bool:
    for j in range(0, len(poly.points)):
        if not is_convex_vertex(prev_vertex, current_vertex, next_vertex) or (
                not (poly.points[j] in (prev_vertex, current_vertex, next_vertex)) and PointInTriangle(poly.points[j],
                                                                                                       triangle(
                                                                                                           prev_vertex,
                                                                                                           current_vertex,
                                                                                                           next_vertex))):
            return False

    return True


# def is_ear_1(prev_vertex, current_vertex, next_vertex, poly: Polygon) -> bool:
#     for j in range(0, len(poly.points)):
#         if not poly.points[j] in (prev_vertex, current_vertex, next_vertex) and \
#                 not PointInTriangle(poly.points[j], triangle(prev_vertex, current_vertex, next_vertex)) \
#                 and is_covex_vertex(prev_vertex, current_vertex, next_vertex):
#             return True
#
#     return False


def ear_clipping(filename) -> List[triangle]:
    triangles = []
    ears = []
    segments = []
    input_list = create_coordinates(filename)
    poly = Polygon(get_simple_polygon(input_list))

    if poly.convexPolygon():

        for i in range(0, len(poly.points) - 2):
            triangles.append(triangle(poly.points[0], poly.points[i + 1], poly.points[(i + 2)]))

        return triangles

    else:
        num_of_points = len(poly.points)

        for i in range(num_of_points):

            prev_vertex = poly.points[(i - 1) % num_of_points]
            curr_vertex = poly.points[i]
            next_vertex = poly.points[(i + 1) % num_of_points]

            if is_ear(prev_vertex, curr_vertex, next_vertex, poly):
                ears.append(curr_vertex)

        while ears and num_of_points >= 3:

            ear = ears.pop(0)
            i = poly.points.index(ear)
            prev_point = poly.points[(i - 1) % (num_of_points)]
            next_point = poly.points[(i + 1) % (num_of_points)]

            poly.points.remove(ear)

            # izbrisemo jednu tacku, na poziciji 'i' pa i+2 nakon brisanja postaje i + 1 -- next_next_vertex
            num_of_points -= 1
            triangles.append(triangle(prev_point, ear, next_point))

            if num_of_points > 3:

                prev_prev_point = poly.points[(i - 2) % num_of_points]
                next_next_point = poly.points[(i + 1) % num_of_points]

                if is_ear(prev_prev_point, prev_point, next_point, poly):
                    if prev_point not in ears:
                        ears.append(prev_point)
                elif prev_point in ears:
                    ears.remove(prev_point)

                if is_ear(prev_point, next_point, next_next_point, poly):
                    if next_point not in ears:
                        ears.append(next_point)
                elif next_point in ears:
                    ears.remove(next_point)
        print(len(triangles))
        return triangles


## funkcija koja trazi slucajno odabrane tacke u slucajno odabranom trouglu triangulacije poligona
# dodano je ogranicenje da se ne moze dva puta izabrati isti trougao


def find_guards_inside_random_triangle(filename) -> Tuple[List[point], List[segment]]:

    input_list = create_coordinates(filename)
    segments = []
    polygon = Polygon(get_simple_polygon(input_list))
    print('poly.points', len(polygon.points))

    triangles = triangulation_ear_clipping(filename)

    print('poly.points', len(polygon.points))

    guards = []
    visible_vertex = []


    visited_triangles = []

    while len(visible_vertex) < len(polygon.points):

        print("novi while")
        n = random.randint(0, len(triangles)-1)
        rand_triangle = triangles[n]
        while rand_triangle in visited_triangles:
            n = random.randint(0, len(triangles)-1)
            rand_triangle = triangles[n]
        visited_triangles.append(rand_triangle)

        print("izabrao random trougao")
        rand_point = point_on_triangle(rand_triangle.first, rand_triangle.second, rand_triangle.third)

        for vertex in polygon.points:
            print("vertex", vertex)

            if vertex not in visible_vertex:
                s = segment(rand_point, vertex)

                if not IntersectionP1(polygon, s):

                    print("provjerio za jedan vertex")
                    visible_vertex.append(vertex)
                    segments.append(s)
                    if rand_point not in guards:
                        guards.append(rand_point)
                        print("dosao do guarda")
    # for t in triangles:
    #     t.draw()


    return guards, segments


def point_on_triangle(pt1: point, pt2: point, pt3: point):
    """
    Random point on the triangle with vertices pt1, pt2 and pt3.
    """
    s, t = sorted([random.random(), random.random()])
    return point(s * pt1[0] + (t-s)*pt2[0] + (1-t)*pt3[0],
            s * pt1[1] + (t-s)*pt2[1] + (1-t)*pt3[1])




#
# p = generate_polygon()
#
# print(len(p.points))
#
# triangles = triangulation(p)
#
# for t in triangles:
#     t.draw()
# p.draw()


# for i in range(0, len(p.points)):
#     print(is_ear(p.points[(i-1) % len(p.points)], p.points[i % len(p.points)], p.points[(i+1) % len(p.points)], p))
# p.draw()



# p = create_coordinates('randsimple-20-25')
# polygon = Polygon(get_simple_polygon(p))
#
# guards = find_guards_inside_random_triangle('randsimple-20-25')
# for guard in guards:
#     guard.draw()
# print(len(guards))



def try_n_times_random_point_random_triangle(n: int, filename)->Tuple[List[point], List[segment]]:
    start_time = time.time()

    min = 100
    final_guards = []
    segments = []
    final_segments = []
    for i in range(0, n):
        guards = find_guards_inside_random_triangle(filename)[0]
        segments = find_guards_inside_random_triangle(filename)[1]
        if min > len(guards):
            min = len(guards)
            final_guards = guards
            final_segments = segments

    print(min)
    print('final guards', final_guards)
    print("--- %s seconds ---" % (time.time() - start_time))

    return final_guards, segments


# funkcija za pronalazak cuvara uzimajuci teziste random trougla
# dodano je ogranicenje da se ne moze dva puta izabrati isti trougao


def find_center_guards_in_random_triangle(filename) -> List[point]:

    input_list = create_coordinates(filename)

    polygon = Polygon(get_simple_polygon(input_list))
    poly = Polygon(get_simple_polygon(input_list))
    print('poly.points', len(polygon.points))

    triangles = triangulation_ear_clipping(filename)

    print('poly.points', len(polygon.points))

    guards = []
    visible_vertex = []


    visited_triangles = []

    while len(visible_vertex) < len(polygon.points):

        print("novi while")
        n = random.randint(0, len(triangles)-1)
        rand_triangle = triangles[n]
        while rand_triangle in visited_triangles:
            n = random.randint(0, len(triangles)-1)
            rand_triangle = triangles[n]
        visited_triangles.append(rand_triangle)

        print("izabrao random trougao")

        rand_point = point((rand_triangle.first.x + rand_triangle.second.x + rand_triangle.third.x)/3, (rand_triangle.first.y +rand_triangle.second.y+rand_triangle.third.y)/3)

        for vertex in polygon.points:
            print("vertex", vertex)

            if vertex not in visible_vertex:
                s = segment(rand_point, vertex)

                if not IntersectionP1(polygon, s):

                    print("provjerio za jedan vertex")
                    visible_vertex.append(vertex)
                    if rand_point not in guards:
                        guards.append(rand_point)
                        print("dosao do guarda")
    # for t in triangles:
    #     t.draw()

    return guards



def try_n_times_center_point_random_triangle(n: int, filename)->List[point]:
    start_time = time.time()

    min = 100
    final_guards = []
    for i in range(0, n):
        guards = find_center_guards_in_random_triangle(filename)
        if min > len(guards):
            min = len(guards)
            final_guards = guards

    print(min)
    print('final guards', final_guards)
    print("--- %s seconds ---" % (time.time() - start_time))

    return final_guards



#funkcija za pronalazak cuvara koji se nalaze na random vrhu random trougla
# dodano je ogranicenje da se ne moze dva puta izabrati isti trougao

def find_vertex_guards_of_random_triangle(filename) -> List[point]:

    input_list = create_coordinates(filename)

    polygon = Polygon(get_simple_polygon(input_list))
    poly = Polygon(get_simple_polygon(input_list))
    print('poly.points', len(polygon.points))

    triangles = triangulation_ear_clipping(filename)

    print('poly.points', len(polygon.points))

    guards = []
    visible_vertex = []


    visited_triangles = []

    while len(visible_vertex) < len(polygon.points):

        print("novi while")
        n = random.randint(0, len(triangles)-1)
        rand_triangle = triangles[n]
        while rand_triangle in visited_triangles:
            n = random.randint(0, len(triangles)-1)
            rand_triangle = triangles[n]
        visited_triangles.append(rand_triangle)

        print("izabrao random trougao")

        choices = [rand_triangle.first, rand_triangle.second, rand_triangle.third]
        rand_point = random.choice(choices)

        for vertex in polygon.points:
            print("vertex", vertex)

            if vertex not in visible_vertex:
                s = segment(rand_point, vertex)

                if not IntersectionP1(polygon, s):

                    print("provjerio za jedan vertex")
                    visible_vertex.append(vertex)
                    if rand_point not in guards:
                        guards.append(rand_point)
                        print("dosao do guarda")
    # for t in triangles:
    #     t.draw()

    return guards




def try_n_times_find_vertex_guards_of_random_triangle(n: int, filename)->List[point]:
    start_time = time.time()

    min = 100
    final_guards = []
    for i in range(0, n):
        guards = find_vertex_guards_of_random_triangle(filename)
        if min > len(guards):
            min = len(guards)
            final_guards = guards

    print(min)
    print('final guards', final_guards)
    print("--- %s seconds ---" % (time.time() - start_time))

    return final_guards
#
# triangles = ear_clipping(Polygon(get_simple_polygon(create_coordinates('randsimple-20-25'))))
# for t in triangles:
#     t.draw()
# for guard in guards:
#     guard.draw()
#
# print(len(guards))
# turtle.done()

def triangulation_ear_clipping(filename)->List[triangle]:
    triangles = []
    ears = []

    segments = []
    input_list = create_coordinates(filename)
    poly = Polygon(get_simple_polygon(input_list))
    num_of_triangles = len(poly.points) - 2

    if poly.convexPolygon():

        for i in range(0, len(poly.points) - 2):
            triangles.append(triangle(poly.points[0], poly.points[i + 1], poly.points[(i + 2)]))

        return triangles

    else:

        print('else block')
        num_of_points = len(poly.points)
        while len(triangles) < num_of_triangles:


            for i in range(0, len(poly.points)):


                print(i)
                curr_point = poly.points[i]
                prev_point = poly.points[(i - 1) % num_of_points]
                next_point = poly.points[(i + 1) % num_of_points]
                next_next_point = poly.points[(i + 2) % (num_of_points)]
                diagonal = segment(prev_point, next_point)


                if is_convex_vertex( next_point, next_next_point, curr_point):
                    if orientation(next_point, prev_point, curr_point) > 0 and orientation(prev_point, next_point, next_next_point) > 0 and not IntersectionP1(poly, diagonal):
                        ears.append(curr_point)
                else:
                    if orientation(next_point, prev_point, next_next_point) < 0 or orientation(prev_point, next_point, curr_point) < 0 and not IntersectionP1(poly, diagonal):
                        ears.append(curr_point)

            if len(ears) == 0:
                triangles.append(triangle(poly.points[0], poly.points[1], poly.points[2]))
            print('ears', ears)
            for i in range(0, len(ears)):
                print('len ears', len(ears))
                ear = ears[i]
                j = poly.points.index(ear)
                prev_point = poly.points[(j - 1) % (num_of_points)]
                next_point = poly.points[(j + 1) % (num_of_points)]
                triangles.append(triangle(prev_point, ear, next_point))
                poly.points.remove(ear)
                num_of_points -= 1
            print('len of triangles', len(triangles))
            ears.clear()


        return triangles


#triangles = triangulation_ear_clipping('randsimple-20-25')
# for t in triangles:
#     t.draw()
#
# turtle.done()


#
# l = [1, 2, 3, 4, 5, 6]
#
# for i in range(0, len(l)):
#     print(l[(i-1) % len(l)])