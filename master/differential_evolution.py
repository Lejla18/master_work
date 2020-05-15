from master.coordinates import create_coordinates
from Project1.project1 import *
from structures.Triangle import triangle
from structures.Polygon import Polygon
import random, time, turtle
from master.triangulation import is_convex_vertex
from structures.Point import point
from math import e

#funkcija koja vraca skup reflesnik vrhova poligona - testirano

def reflex_vertices(poly:Polygon)->List[point]:
    reflex_vertices = []

    for i in range(0, len(poly.points)):
        if not is_convex_vertex(poly.points[(i-1)%len(poly.points)], poly.points[i], poly.points[(i+1)%len(poly.points)]):
            reflex_vertices.append(poly.points[i])
   # print(len(reflex_vertices))
    return reflex_vertices


#funkcija koja provjerava da li je neki skup, skup čuvara

# input list je input refleksnih vrhova

def is_guard_set(input_list: List[point], poly: Polygon)->Tuple[bool, List[segment]]:

    visible_vertex = []
    segments = []
    reflex_vertices_minus_one = []

    for p in input_list:

        for vertex in poly.points:
            if vertex not in visible_vertex:
                s = segment(vertex, p)
             # srediste segmenta
                p1 = point((vertex.x + p.x)/2, (vertex.y+p.y)/2)
               #potrebno je provjeriti da li je segment unutar poligona sa PointInsidePolygon(p1, poly):

                if not IntersectionP1(poly, s) and PointInsidePolygon(p1, poly):
                    segments.append(s)
                    visible_vertex.append(vertex)

                # slucaj kada se segmenti preklapaju, tj kada cuvar sa refleksne ivice vidi susjedni vrh
                else:
                    for i in range(0, len(poly.points)):
                        seg = segment(poly.points[i], poly.points[(i+1) % len(poly.points)])
                        if same_segments(seg, s):
                            visible_vertex.append(vertex)
                            segments.append(s)

    print('visible vertex', len(visible_vertex))
    print('poly points', len(poly.points))

    return len(visible_vertex) == len(poly.points), segments



#vraca skup inicijalne populacije, skup pocetnih cuvara
#vraca skup cuvara sa tackama, i skup cuvara binarno (1 na mjestu tacke koja je cuvar, 0 na mjestu koja nije cuvar- duziana binarna je
# kao i duzina poly.points )

def create_init_population(reflex_vertices:List[point], poly:Polygon)->Tuple[List[List[point]], List[List[int]]]:

    init_population = []
    init_population_binary = []

    bin = []
    for i in range(0, len(poly.points)):
        bin.append(0)
    print(bin)

    for i in range(0, len(reflex_vertices)):


        r_ver = reflex_vertices.copy()
        #print('kopirana')
        #print(r_ver)
        #print('i', i)
        del r_ver[i]
        #print('nakon brisanja')
        #print(r_ver)



        if is_guard_set(r_ver, poly)[0]:

            l = bin.copy()
            init_population.append(r_ver)
            for s in range(0, len(poly.points)):
                if poly.points[s] in r_ver:
                    l[s] = 1
            init_population_binary.append(l)

        else:
            if len(init_population) < 4:
                init_population.append(reflex_vertices)
                l = bin.copy()
                for m in range(0, len(poly.points)):
                    if poly.points[m] in r_ver:
                        l[m] = 1
                init_population_binary.append(l)

    print('init population', len(init_population))

    print(poly.points)
    print(init_population_binary[0])
    print(init_population[0])

    return init_population, init_population_binary



def sigmoid_opeataion(n:float)->int:
    i = 1/(1+e**n)
    rand = random.random()
    if rand < i:
        return 1
    else:
        return 0

def create_mutant_vector(current_population:List[List[int]]):

    for i in range(0, len(current_population)):

        mutant_vector = []
        mutant_vector_temp = []

        F = 0.6

        rez = []

        target_vector = current_population[i]

        r_0 = random.randint(0, len(current_population)-1)

        while current_population[r_0] == target_vector:
            r_0 = random.randint(0, len(current_population)-1)

        base_vector = current_population[r_0]

        r_1 = random.randint(0, len(current_population)-1)

        while current_population[r_1] == target_vector or current_population[r_1] == base_vector:
            r_1 = random.randint(0, len(current_population)-1)

        r_1_vector = current_population[r_1]

        r_2 = random.randint(0, len(current_population)-1)

        while current_population[r_2] == target_vector or current_population[r_2] == base_vector or current_population[r_2] == r_1_vector:
            r_2 = random.randint(0, len(current_population)-1)

        r_2_vector = current_population[r_2]
        rez = [(x - y)*F for x ,y in zip(r_1_vector, r_2_vector)]

        print(rez)
        mutant_vector_temp = [x + y for x,y in zip(base_vector, rez)]
        mutant_vector = [sigmoid_opeataion(x) for x in mutant_vector_temp]

        print(mutant_vector)



p = create_coordinates('randsimple-20-25')
polygon = Polygon(get_simple_polygon(p))

test = create_init_population(reflex_vertices(polygon), polygon)

create_mutant_vector(test[1])
print(len(test[1]))

#
# p = create_coordinates('randsimple-20-1')
# polygon = Polygon(get_simple_polygon(p))
#
# reflex_verticess = reflex_vertices(polygon)
#
# result = is_guard_set(reflex_verticess, polygon)
#
# print(result[0])


#
# def differential_evolution(filename)->Tuple[List[point]]:
#
#     input_list = create_coordinates(filename)
#     polygon = Polygon(get_simple_polygon(input_list))
#
#

#
#
#



