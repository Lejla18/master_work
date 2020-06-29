from master.coordinates import create_coordinates
from Project1.project1 import *
from master.triangulation_algorithm import earclip
from structures.Triangle import triangle
from structures.Polygon import Polygon
import random, time, turtle


def is_convex_vertex(pprev: point, pcurr: point, pnext: point) -> bool:
    return orientation(pprev, pcurr, pnext) > 0


def _triangle_area(x1, y1, x2, y2, x3, y3):
    return abs((x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2.0)



# def is_ear(prev_vertex, current_vertex, next_vertex, poly: Polygon) -> bool:
#     for j in range(0, len(poly.points)):
#         if not is_convex_vertex(prev_vertex, current_vertex, next_vertex) or (
#                 not (poly.points[j] in (prev_vertex, current_vertex, next_vertex)) and PointInTriangle(poly.points[j],
#                                                                                                        triangle(
#                                                                                                            prev_vertex,
#                                                                                                            current_vertex,
#                                                                                                            next_vertex))):
#             return False
#
#     return True



def is_ear(prev_vertex, current_vertex, next_vertex, poly: Polygon) -> bool:
    for j in range(0, len(poly.points)):
        if is_convex_vertex(prev_vertex, current_vertex, next_vertex) and \
                not(PointInTriangle(poly.points[j], triangle(prev_vertex,current_vertex, next_vertex))) and \
                _triangle_area(prev_vertex.x, prev_vertex.y, current_vertex.x, current_vertex.y, next_vertex.x, next_vertex.y) > 0 and \
                    not (poly.points[j] in (prev_vertex, current_vertex, next_vertex)):

            return True

    return False

# prev prev = Tn-1
# prev = T0
# curr = T1
#nex = T2


def is_ear_1(prev_prev_vertex, prev_vertex, current_vertex, next_vertex, poly: Polygon) -> bool:
        if is_convex_vertex(prev_vertex, current_vertex, next_vertex):
            if orientation(current_vertex, prev_prev_vertex, prev_vertex) > 0 and orientation(prev_prev_vertex, current_vertex, next_vertex):
                return True
        elif not(is_convex_vertex(prev_vertex, current_vertex, next_vertex)):
            if orientation(current_vertex, prev_prev_vertex, next_vertex) < 0 or orientation(prev_prev_vertex, current_vertex, prev_vertex) < 0:
                return True
        return False







def ear_clipping(filename) -> List[triangle]:
    triangles = []
    ears = []
    segments = []
    input_list = create_coordinates(filename)
    poly = Polygon(input_list)

    if poly.convexPolygon():

        for i in range(0, len(poly.points) - 2):
            triangles.append(triangle(poly.points[0], poly.points[i + 1], poly.points[(i + 2)]))

        return triangles

    else:
        num_of_points = len(poly.points)

        # for i in range(num_of_points):
        #
        #     prev_vertex = poly.points[(i - 1) % num_of_points]
        #     curr_vertex = poly.points[i]
        #     next_vertex = poly.points[(i + 1) % num_of_points]
        #
        #     if is_ear(prev_vertex, curr_vertex, next_vertex, poly):
        #         ears.append(curr_vertex)
        #
        # while ears and num_of_points >= 3:
        #
        #     ear = ears.pop(0)
        #     i = poly.points.index(ear)
        #     prev_point = poly.points[(i - 1) % (num_of_points)]
        #     next_point = poly.points[(i + 1) % (num_of_points)]
        #
        #     poly.points.remove(ear)
        #
        #     # izbrisemo jednu tacku, na poziciji 'i' pa i+2 nakon brisanja postaje i + 1 -- next_next_vertex
        #     num_of_points -= 1
        #     triangles.append(triangle(prev_point, ear, next_point))
        #
        #     if num_of_points > 3:
        #
        #         prev_prev_point = poly.points[(i - 2) % num_of_points]
        #         next_next_point = poly.points[(i + 1) % num_of_points]
        #
        #         if is_ear(prev_prev_point, prev_point, next_point, poly):
        #             if prev_point not in ears:
        #                 ears.append(prev_point)
        #         elif prev_point in ears:
        #             ears.remove(prev_point)
        #
        #         if is_ear(prev_point, next_point, next_next_point, poly):
        #             if next_point not in ears:
        #                 ears.append(next_point)
        #         elif next_point in ears:
        #             ears.remove(next_point)
        # print(len(triangles))
        # return triangles
        i = 0
        while num_of_points >= 3:

            if is_ear_1(poly.points[(i-2) % num_of_points], poly.points[(i-1) % num_of_points], poly.points[i], poly.points[(i+1) % num_of_points], poly):
                triangles.append(triangle(poly.points[(i-1) % num_of_points], poly.points[i], poly.points[(i+1)%num_of_points]))
                poly.points.remove(i)
                num_of_points = num_of_points - 1
                i = 0
            else:
                i = i + 1
        return triangles

## funkcija koja trazi slucajno odabrane tacke u slucajno odabranom trouglu triangulacije poligona
# dodano je ogranicenje da se ne moze dva puta izabrati isti trougao


def find_guards_inside_random_triangle(filename) -> Tuple[List[point], List[segment]]:

    input_list = create_coordinates(filename)
    segments = []
    polygon = Polygon(input_list)
    #print('poly.points', len(polygon.points))

    triangles = earclip(filename)

    #print('poly.points', len(polygon.points))

    guards = []
    visible_vertex = []


    visited_triangles = []

    while len(visible_vertex) < len(polygon.points):

        #print("novi while")
        n = random.randint(0, len(triangles)-1)
        rand_triangle = triangles[n]
        while rand_triangle in visited_triangles and len(visited_triangles) < 18:
            n = random.randint(0, len(triangles)-1)
            rand_triangle = triangles[n]
        visited_triangles.append(rand_triangle)

        #print("izabrao random trougao")
        rand_point = point_on_triangle(rand_triangle.first, rand_triangle.second, rand_triangle.third)

        for vertex in polygon.points:
            #print("vertex", vertex)

            if vertex not in visible_vertex:
                s = segment(rand_point, vertex)
                p1 = point((vertex.x + rand_point.x)/2, (vertex.y+rand_point.y)/2)

                if not IntersectionP1(polygon, s) and PointInsidePolygon(p1, polygon):

                    #print("provjerio za jedan vertex")
                    visible_vertex.append(vertex)
                    segments.append(s)
                    if rand_point not in guards:
                        guards.append(rand_point)
                        #print("dosao do guarda")
                    else:
                        for i in range(0, len(polygon.points)):
                            seg = segment(polygon.points[i], polygon.points[(i + 1) % len(polygon.points)])
                            if same_segments(seg, s):
                                visible_vertex.append(vertex)
                                segments.append(s)
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
# polygon = Polygon(p)
#
# guards = find_guards_inside_random_triangle('randsimple-20-25')
# for guard in guards:
#     guard.draw()
# print(len(guards))



def try_n_times_random_point_random_triangle(n: int, filename)-> List[point]:

    start_time = time.time()
    min = 100
    max = 0
    final_guards = []
    rjesenje = []
    srednja = 0
    vrijeme = 0
    t = time.time()
    for i in range(0, n):
        #print('novi krug')
        start_time = time.time()
        guards = find_guards_inside_random_triangle(filename)[0]
        rjesenje.append(len(guards))
        vrijeme = vrijeme + (time.time() - start_time)
        if min > len(guards):
            min = len(guards)
            final_guards = guards
        if max < len(guards):
            max = len(guards)
        srednja = srednja + len(guards)
    print('jedno rjesenje', rjesenje)
    print('max', max)
    print('srednja', srednja/n)
    print('min', min)
    print('srednje vrijeme', vrijeme/n)
    print("--- %s seconds ---" % (time.time() - t))

    return final_guards


# funkcija za pronalazak cuvara uzimajuci teziste random trougla
# dodano je ogranicenje da se ne moze dva puta izabrati isti trougao


def find_center_guards_in_random_triangle(filename) -> List[point]:

    input_list = create_coordinates(filename)

    polygon = Polygon(input_list)
    #print('poly.points', len(polygon.points))

    triangles = earclip(filename)

    #print('poly.points', len(polygon.points))

    guards = []
    visible_vertex = []


    visited_triangles = []

    while len(visible_vertex) < len(polygon.points):

        #print("novi while")
        n = random.randint(0, len(triangles)-1)
        rand_triangle = triangles[n]
        while rand_triangle in visited_triangles and len(visited_triangles) < 18:
            n = random.randint(0, len(triangles)-1)
            rand_triangle = triangles[n]
        visited_triangles.append(rand_triangle)

        #print("izabrao random trougao")

        rand_point = point((rand_triangle.first.x + rand_triangle.second.x + rand_triangle.third.x)/3, (rand_triangle.first.y +rand_triangle.second.y+rand_triangle.third.y)/3)

        for vertex in polygon.points:
            #print("vertex", vertex)

            if vertex not in visible_vertex:
                s = segment(rand_point, vertex)
                p1 = point((vertex.x + rand_point.x)/2, (vertex.y+rand_point.y)/2)

                if not IntersectionP1(polygon, s) and PointInsidePolygon(p1, polygon):

                    #print("provjerio za jedan vertex")
                    visible_vertex.append(vertex)
                    if rand_point not in guards:
                        guards.append(rand_point)
                        #print("dosao do guarda")
    # for t in triangles:
    #     t.draw()

    return guards



def try_n_times_center_point_random_triangle(n: int, filename)->List[point]:
    jedno_rjesenje = []
    sum = 0
    min = 100
    max = 0
    ukupno = time.time()
    srednja = 0
    final_guards = []
    for i in range(0, n):
        print('novi krug :')
        start_time = time.time()
        guards = find_center_guards_in_random_triangle(filename)
        print(i, 'to rjesenje', len(guards))
        jedno_rjesenje.append(len(guards))
        sum = sum + (time.time() - start_time)
        if min > len(guards):
            min = len(guards)
            final_guards = guards
        if max < len(guards):
            max = len(guards)
        srednja = srednja + len(guards)
    print(jedno_rjesenje)

    print('prosjecno vrijeme', sum/n)
    print('max', max)
    print('srednja', srednja/n)
    print('min', min)
    #print('final guards', final_guards)
    print("--- %s seconds ---" % (time.time() - ukupno))

    return final_guards



#funkcija za pronalazak cuvara koji se nalaze na random vrhu random trougla
# dodano je ogranicenje da se ne moze dva puta izabrati isti trougao

def find_vertex_guards_of_random_triangle(filename) -> List[point]:

    input_list = create_coordinates(filename)

    polygon = Polygon(input_list)
    print('poly.points', len(polygon.points))

    triangles = earclip(filename)

    print('poly.points', len(polygon.points))

    guards = []
    visible_vertex = []


    visited_triangles = []
    rand_triangle = []
    unvisible = []
    while len(visible_vertex) < len(polygon.points):

        print('visible vertex', len(visible_vertex))


        print("novi while")
        n = random.randint(0, len(triangles) - 1)
        print(n)
        rand_triangle = triangles[n]
        while rand_triangle in visited_triangles and len(visited_triangles) < 14:
            n = random.randint(0, len(triangles) - 1)
            rand_triangle = triangles[n]
            visited_triangles.append(rand_triangle)


        print("izabrao random trougao")

        choices = [rand_triangle.first, rand_triangle.second, rand_triangle.third]
        rand_point = random.choice(choices)


        for vertex in polygon.points:
            print("vertex", vertex)
            if vertex not in visible_vertex:
                s = segment(rand_point, vertex)
                p1 = point((vertex.x + rand_point.x)/2, (vertex.y+rand_point.y)/2)

                if not IntersectionP1(polygon, s) and PointInsidePolygon(p1, polygon):

                    print("provjerio za jedan vertex")
                    visible_vertex.append(vertex)
                    if rand_point not in guards:
                        guards.append(rand_point)
                        print("dosao do guarda")
                    else:
                        for i in range(0, len(polygon.points)):
                            seg = segment(polygon.points[i], polygon.points[(i + 1) % len(polygon.points)])
                            if same_segments(seg, s):
                                visible_vertex.append(vertex)
    # for t in triangles:
    #     t.draw()

    return guards




def try_n_times_find_vertex_guards_of_random_triangle(n: int, filename)->List[point]:
    start_time = time.time()

    min = 100
    max = 0
    srednja = 0
    final_guards = []
    for i in range(0, n):
        guards = find_vertex_guards_of_random_triangle(filename)
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
#
# triangles = ear_clipping(Polygon(get_simple_polygon(create_coordinates('randsimple-80-25'))))
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
    poly = Polygon(input_list)
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


#triangles = triangulation_ear_clipping('randsimple-80-25')
# for t in triangles:
#     t.draw()
#
# turtle.done()


#
# l = [1, 2, 3, 4, 5, 6]
#
# for i in range(0, len(l)):
#     print(l[(i-1) % len(l)])
#
#
# print('20-1', try_n_times_random_point_random_triangle(30, 'randsimple-20-1'))
#
# print('20-2', try_n_times_random_point_random_triangle(30, 'randsimple-20-2'))
#
# print('20-3', try_n_times_random_point_random_triangle(30, 'randsimple-20-3'))
#
# print('20-4', try_n_times_random_point_random_triangle(30, 'randsimple-20-4'))
#
# print('20-5', try_n_times_random_point_random_triangle(30, 'randsimple-20-5'))
#
# print('20-6', try_n_times_random_point_random_triangle(30, 'randsimple-20-6'))
#
# print('20-7', try_n_times_random_point_random_triangle(30, 'randsimple-20-7'))
#
# print('20-8', try_n_times_random_point_random_triangle(30, 'randsimple-20-8'))
#
# print('20-9', try_n_times_random_point_random_triangle(30, 'randsimple-20-9'))
#
# print('20-10', try_n_times_random_point_random_triangle(30, 'randsimple-20-10'))
#
# print('20-11', try_n_times_random_point_random_triangle(30, 'randsimple-20-11'))
#
# print('20-12', try_n_times_random_point_random_triangle(30, 'randsimple-20-12'))
#
# print('20-13', try_n_times_random_point_random_triangle(30, 'randsimple-20-13'))
#
# print('20-14', try_n_times_random_point_random_triangle(30, 'randsimple-20-14'))
#
# print('20-15', try_n_times_random_point_random_triangle(30, 'randsimple-20-15'))
#
# print('20-16', try_n_times_random_point_random_triangle(30, 'randsimple-20-16'))
#
# print('20-17', try_n_times_random_point_random_triangle(30, 'randsimple-20-17'))
#
# print('20-18', try_n_times_random_point_random_triangle(30, 'randsimple-20-18'))
#
# print('20-19', try_n_times_random_point_random_triangle(30, 'randsimple-20-19'))
#
# print('20-80', try_n_times_random_point_random_triangle(30, 'randsimple-20-20'))
#
# print('20-21', try_n_times_random_point_random_triangle(30, 'randsimple-20-21'))
#
# print('20-22', try_n_times_random_point_random_triangle(30, 'randsimple-20-22'))
#
# print('20-23', try_n_times_random_point_random_triangle(30, 'randsimple-20-23'))
#
# print('20-24', try_n_times_random_point_random_triangle(30, 'randsimple-20-24'))
#
# print('20-25', try_n_times_random_point_random_triangle(30, 'randsimple-20-25'))
#
# print('20-26', try_n_times_random_point_random_triangle(30, 'randsimple-20-26'))
#
# print('20-27', try_n_times_random_point_random_triangle(30, 'randsimple-20-27'))
#
# print('20-28', try_n_times_random_point_random_triangle(30, 'randsimple-20-28'))
#
# print('20-29', try_n_times_random_point_random_triangle(30, 'randsimple-20-29'))
#
# print('20-30', try_n_times_random_point_random_triangle(30, 'randsimple-20-30'))
#
#
# print('40-1', try_n_times_random_point_random_triangle(30, 'randsimple-40-1'))
#
# print('40-2', try_n_times_random_point_random_triangle(30, 'randsimple-40-2'))
#
# print('40-3', try_n_times_random_point_random_triangle(30, 'randsimple-40-3'))
#
# print('40-4', try_n_times_random_point_random_triangle(30, 'randsimple-40-4'))
#
# print('40-5', try_n_times_random_point_random_triangle(30, 'randsimple-40-5'))
#
# print('40-6', try_n_times_random_point_random_triangle(30, 'randsimple-40-6'))
#
# print('40-7', try_n_times_random_point_random_triangle(30, 'randsimple-40-7'))
#
# print('40-8', try_n_times_random_point_random_triangle(30, 'randsimple-40-8'))
#
# print('40-9', try_n_times_random_point_random_triangle(30, 'randsimple-40-9'))
#
# print('40-10', try_n_times_random_point_random_triangle(30, 'randsimple-40-10'))
#
# print('40-11', try_n_times_random_point_random_triangle(30, 'randsimple-40-11'))
#
# print('40-12', try_n_times_random_point_random_triangle(30, 'randsimple-40-12'))
#
# print('40-13', try_n_times_random_point_random_triangle(30, 'randsimple-40-13'))
#
# print('40-14', try_n_times_random_point_random_triangle(30, 'randsimple-40-14'))
#
# print('40-15', try_n_times_random_point_random_triangle(30, 'randsimple-40-15'))
#
# print('40-16', try_n_times_random_point_random_triangle(30, 'randsimple-40-16'))
#
# print('40-17', try_n_times_random_point_random_triangle(30, 'randsimple-40-17'))
#
# print('40-18', try_n_times_random_point_random_triangle(30, 'randsimple-40-18'))
#
# print('40-19', try_n_times_random_point_random_triangle(30, 'randsimple-40-19'))
#
# print('40-20', try_n_times_random_point_random_triangle(30, 'randsimple-40-20'))
#
# print('40-21', try_n_times_random_point_random_triangle(30, 'randsimple-40-21'))
#
# print('40-22', try_n_times_random_point_random_triangle(30, 'randsimple-40-22'))
#
# print('40-23', try_n_times_random_point_random_triangle(30, 'randsimple-40-23'))
#
# print('40-24', try_n_times_random_point_random_triangle(30, 'randsimple-40-24'))
#
# print('40-25', try_n_times_random_point_random_triangle(30, 'randsimple-40-25'))
#
# print('40-26', try_n_times_random_point_random_triangle(30, 'randsimple-40-26'))
#
# print('40-27', try_n_times_random_point_random_triangle(30, 'randsimple-40-27'))
#
# print('40-28', try_n_times_random_point_random_triangle(30, 'randsimple-40-28'))
#
# print('40-29', try_n_times_random_point_random_triangle(30, 'randsimple-40-29'))
#
# print('40-30', try_n_times_random_point_random_triangle(30, 'randsimple-40-30'))
#
# print('60-1', try_n_times_random_point_random_triangle(30, 'randsimple-60-1'))
#
# print('60-2', try_n_times_random_point_random_triangle(30, 'randsimple-60-2'))
#
# print('60-3', try_n_times_random_point_random_triangle(30, 'randsimple-60-3'))
#
# print('60-4', try_n_times_random_point_random_triangle(30, 'randsimple-60-4'))
#
# print('60-5', try_n_times_random_point_random_triangle(30, 'randsimple-60-5'))
#
# print('60-6', try_n_times_random_point_random_triangle(30, 'randsimple-60-6'))
#
# print('60-7', try_n_times_random_point_random_triangle(30, 'randsimple-60-7'))
#
# print('60-8', try_n_times_random_point_random_triangle(30, 'randsimple-60-8'))
#
# print('60-9', try_n_times_random_point_random_triangle(30, 'randsimple-60-9'))
#
# print('60-10', try_n_times_random_point_random_triangle(30, 'randsimple-60-10'))
#
# print('60-11', try_n_times_random_point_random_triangle(30, 'randsimple-60-11'))
#
# print('60-12', try_n_times_random_point_random_triangle(30, 'randsimple-60-12'))
#
# print('60-13', try_n_times_random_point_random_triangle(30, 'randsimple-60-13'))
#
# print('60-14', try_n_times_random_point_random_triangle(30, 'randsimple-60-14'))
#
# print('60-15', try_n_times_random_point_random_triangle(30, 'randsimple-60-15'))
#
# print('60-16', try_n_times_random_point_random_triangle(30, 'randsimple-60-16'))
#
# print('60-17', try_n_times_random_point_random_triangle(30, 'randsimple-60-17'))
#
# print('60-18', try_n_times_random_point_random_triangle(30, 'randsimple-60-18'))
#
# print('60-19', try_n_times_random_point_random_triangle(30, 'randsimple-60-19'))
#
# print('60-80', try_n_times_random_point_random_triangle(30, 'randsimple-60-20'))
#
# print('60-21', try_n_times_random_point_random_triangle(30, 'randsimple-60-21'))
#
# print('60-22', try_n_times_random_point_random_triangle(30, 'randsimple-60-22'))
#
# print('60-23', try_n_times_random_point_random_triangle(30, 'randsimple-60-23'))
#
# print('60-24', try_n_times_random_point_random_triangle(30, 'randsimple-60-24'))
#
# print('60-25', try_n_times_random_point_random_triangle(30, 'randsimple-60-25'))
#
# print('60-26', try_n_times_random_point_random_triangle(30, 'randsimple-60-26'))
#
# print('60-27', try_n_times_random_point_random_triangle(30, 'randsimple-60-27'))
#
# print('60-28', try_n_times_random_point_random_triangle(30, 'randsimple-60-28'))
#
# print('60-29', try_n_times_random_point_random_triangle(30, 'randsimple-60-29'))
#
# print('60-30', try_n_times_random_point_random_triangle(30, 'randsimple-60-30'))
#
# print('80-1', try_n_times_random_point_random_triangle(30, 'randsimple-80-1'))
#
# print('80-2', try_n_times_random_point_random_triangle(30, 'randsimple-80-2'))
#
# print('80-3', try_n_times_random_point_random_triangle(30, 'randsimple-80-3'))
#
# print('80-4', try_n_times_random_point_random_triangle(30, 'randsimple-80-4'))
#
# print('80-5', try_n_times_random_point_random_triangle(30, 'randsimple-80-5'))
#
# print('80-6', try_n_times_random_point_random_triangle(30, 'randsimple-80-6'))
#
# print('80-7', try_n_times_random_point_random_triangle(30, 'randsimple-80-7'))
#
# print('80-8', try_n_times_random_point_random_triangle(30, 'randsimple-80-8'))
#
# print('80-9', try_n_times_random_point_random_triangle(30, 'randsimple-80-9'))
#
# print('80-10', try_n_times_random_point_random_triangle(30, 'randsimple-80-10'))
#
# print('80-11', try_n_times_random_point_random_triangle(30, 'randsimple-80-11'))
#
# print('80-12', try_n_times_random_point_random_triangle(30, 'randsimple-80-12'))
#
# print('80-13', try_n_times_random_point_random_triangle(30, 'randsimple-80-13'))
#
# print('80-14', try_n_times_random_point_random_triangle(30, 'randsimple-80-14'))
#
# print('80-15', try_n_times_random_point_random_triangle(30, 'randsimple-80-15'))
#
# print('80-16', try_n_times_random_point_random_triangle(30, 'randsimple-80-16'))
#
# print('80-17', try_n_times_random_point_random_triangle(30, 'randsimple-80-17'))
#
# print('80-18', try_n_times_random_point_random_triangle(30, 'randsimple-80-18'))
#
# print('80-19', try_n_times_random_point_random_triangle(30, 'randsimple-80-19'))
#
# print('80-80', try_n_times_random_point_random_triangle(30, 'randsimple-80-20'))
#
# print('80-21', try_n_times_random_point_random_triangle(30, 'randsimple-80-21'))
#
# print('80-22', try_n_times_random_point_random_triangle(30, 'randsimple-80-22'))
#
# print('80-23', try_n_times_random_point_random_triangle(30, 'randsimple-80-23'))
#
# print('80-24', try_n_times_random_point_random_triangle(30, 'randsimple-80-24'))
#
# print('80-25', try_n_times_random_point_random_triangle(30, 'randsimple-80-25'))
#
# print('80-26', try_n_times_random_point_random_triangle(30, 'randsimple-80-26'))
#
# print('80-27', try_n_times_random_point_random_triangle(30, 'randsimple-80-27'))
#
# print('80-28', try_n_times_random_point_random_triangle(30, 'randsimple-80-28'))
#
# print('80-29', try_n_times_random_point_random_triangle(30, 'randsimple-80-29'))
#
# print('80-30', try_n_times_random_point_random_triangle(30, 'randsimple-80-30'))
#
#
