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
    print(len(reflex_vertices))
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

    #print('visible vertex', len(visible_vertex))
    #print('poly points', len(poly.points))

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
   # print(bin)

    for i in range(0, len(reflex_vertices)):


        r_ver = reflex_vertices.copy()
        #print('kopirana')
        #print(r_ver)
        #print('i', i)
        #print('del', r_ver[i])
        del r_ver[i]

        #r_ver[i] = 0
        #print('nakon brisanja')
        #print(r_ver)



        if is_guard_set(r_ver, poly)[0]:

            l = bin.copy()
            init_population.append(r_ver)
            for s in range(0, len(poly.points)):
                if poly.points[s] in r_ver:
                    l[s] = 1
            init_population_binary.append(l)
            #print('len init population', len(init_population))
            #print(l)
        else:
            if len(init_population) < 4:
                init_population.append(reflex_vertices)
                l = bin.copy()
                for m in range(0, len(poly.points)):
                    if poly.points[m] in r_ver:
                        l[m] = 1
                init_population_binary.append(l)

    # print('init population', len(init_population))
    #
    # print(poly.points)
    # print(init_population_binary[0])
    # print(init_population[0])

    return init_population, init_population_binary



def sigmoid_opeataion(n:float)->int:
    i = 1/(1+e**n)
    rand = random.uniform(0, 1)
    if rand < i:
        return 1
    else:
        return 0



#differential evolution with de_rand_1_bin and uniform crossover

def de_rand_1_bin(current_population_with_points:List[List[point]],current_population:List[List[int]], polygon:Polygon):

    result_vectors = []
    result_point_vectors = []

    for i in range(0, len(current_population)):

        #creating mutant vector

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
        rez = [(x - y)*F for x, y in zip(r_1_vector, r_2_vector)]

        #print(rez)
        mutant_vector_temp = [x + y for x, y in zip(base_vector, rez)]
        mutant_vector = [sigmoid_opeataion(x) for x in mutant_vector_temp]
        #print(mutant_vector)

        #mutant vecotor
        # target vector

        #crossover

        trial_vector = []

        c_r = random.uniform(0, 1)

        j = random.randint(0, len(mutant_vector) - 1)

        for k in range(0, len(mutant_vector)):

            r = random.uniform(0, 1)
            if i == j or r <= c_r:
                trial_vector.append(mutant_vector[k])
            else:
                trial_vector.append(target_vector[k])
        #(print('trial vector'))
        #print(trial_vector)
        #crossovered_vectors.append(trial_vector)

        #selection
        #potrebno je provjeriti da li je trial vector skup cuvara, ukoliko jeste, da li je manji od skupa cuvara target vectora.
        #vraca se vektor sa manjim brojem cuvara

        list_of_points_for_trial_vector = []

        for count in range(0, len(trial_vector)):
            if trial_vector[count] == 1:
                list_of_points_for_trial_vector.append(polygon.points[count])

        if is_guard_set(list_of_points_for_trial_vector, polygon)[0] and len(list_of_points_for_trial_vector) <= target_vector.count(1):
            result_vectors.append(trial_vector)
            result_point_vectors.append(list_of_points_for_trial_vector)
            #print('if')
            #print('is guard set', is_guard_set(list_of_points_for_trial_vector, polygon)[0])
        else:
            result_vectors.append(target_vector)
            #print('else')
            result_point_vectors.append(current_population_with_points[i])
            #print('is guard set', is_guard_set(current_population_with_points[i], polygon)[0])



    return result_point_vectors, result_vectors



def run_de_algorithm(filename)->List[point]:
    start_time = time.time()
    p = create_coordinates(filename)
    polygon = Polygon(p)
    init_population = create_init_population(reflex_vertices(polygon), polygon)
    result = de_rand_1_bin(init_population[0], init_population[1], polygon)


    final = [result]

    # print('init', final)
    #
    # print(len(result[1]))
    # for i in range(0, len(result[1])):
    #     print(result[1][i].count(1))

    #print('num of reflex', len(reflex_vertices(polygon)))

    guards = []
    h = 30
    t = time.time()
    avr_time = 0
    avr_time_post = 0
    for i in range(0, h):
        start_time = time.time()
        start_time_1 = time.time()
        result1 = de_rand_1_bin(final[i][0], final[i][1], polygon)
        avr_time = avr_time + (time.time()-start_time)
        final.append(result1)
        #guards = [result1[0]]
    min = 1000
    max = 0
    position = 0
    srednja = 0
    pos_max = 0

    for k in range(0, len(final[h][1])):
        test = len(postprocessing(final[h][0][k], polygon))
        guards.append(test)
        min_k = final[h][1][k].count(1)
        max_k = final[h][1][k].count(1)
        #print('mink', min_k)
        # if min > min_k:
        #     min = min_k
        #     position = k
        #     guards = final[h][0][k].copy()
        if min > test:
            min = test
            position = k
        # if max < max_k:
        #     max = max_k
        #     pos_max = k
        if max < test:
            max = test
        srednja = srednja + test
    avr_time_post = avr_time_post + start_time_1
            #pos_max = k
        #print('len', len(final[h][1]))
    #print(min)
    #print(position)
    #print('len of guards', len(guards))
    # print(final[h][0])
    # print(final[h][1])


    #print('max guards:', len(postprocessing(final[h][0][pos_max], polygon)), postprocessing(final[h][0][pos_max], polygon))
    #print('min guards -final result:', postprocessing(final[h][0][position], polygon))
    print('guards', guards)
    print('max guards', max)
    print('srednja ', srednja/len(final[h][1]))
    print('min guards', min)
    print('avg bez postprocesinga', avr_time/h)
    print('avg sa postprocesing', avr_time_post / h)
    print("--- %s seconds ---" % (time.time() - t))
    return postprocessing(final[h][0][position], polygon)





def draw_segments(filename):
    p = create_coordinates(filename)
    polygon = Polygon(p)

    result = run_de_algorithm(filename)

    return is_guard_set(result, polygon)[1], result



# ----------------------------------------

# de_best_1_bin

#----------------------------------------




def de_best_1_bin(current_population_with_points:List[List[point]],current_population:List[List[int]], polygon:Polygon):

    result_vectors = []
    result_point_vectors = []

    for i in range(0, len(current_population)):

        #creating mutant vector

        mutant_vector = []
        mutant_vector_temp = []

        F = 0.6

        rez = []

        target_vector = current_population[i]

       #base_vector se bira najbolji iz trenutne populacije
        r_0 = 0
        min_r0 = 500
        for i in range(0, len(current_population)):
            if current_population[i].count(1) < min_r0:
                min_r0 = current_population[i].count(1)
                r_0 = i


        base_vector = current_population[r_0]

        r_1 = random.randint(0, len(current_population)-1)

        while current_population[r_1] == target_vector or current_population[r_1] == base_vector:
            r_1 = random.randint(0, len(current_population)-1)

        r_1_vector = current_population[r_1]

        r_2 = random.randint(0, len(current_population)-1)

        while current_population[r_2] == target_vector or current_population[r_2] == base_vector or current_population[r_2] == r_1_vector:
            r_2 = random.randint(0, len(current_population)-1)

        r_2_vector = current_population[r_2]
        rez = [(x - y)*F for x, y in zip(r_1_vector, r_2_vector)]

        #print(rez)
        mutant_vector_temp = [x + y for x, y in zip(base_vector, rez)]
        mutant_vector = [sigmoid_opeataion(x) for x in mutant_vector_temp]
        #print(mutant_vector)

        #mutant vecotor
        # target vector

        #crossover

        trial_vector = []

        c_r = random.uniform(0, 1)

        j = random.randint(0, len(mutant_vector) - 1)

        for k in range(0, len(mutant_vector)):

            r = random.uniform(0, 1)
            if i == j or r <= c_r:
                trial_vector.append(mutant_vector[k])
            else:
                trial_vector.append(target_vector[k])
        #(print('trial vector'))
        #print(trial_vector)
        #crossovered_vectors.append(trial_vector)

        #selection
        #potrebno je provjeriti da li je trial vector skup cuvara, ukoliko jeste, da li je manji od skupa cuvara target vectora.
        #vraca se vektor sa manjim brojem cuvara

        list_of_points_for_trial_vector = []

        for count in range(0, len(trial_vector)):
            if trial_vector[count] == 1:
                list_of_points_for_trial_vector.append(polygon.points[count])

        if is_guard_set(list_of_points_for_trial_vector, polygon)[0] and len(list_of_points_for_trial_vector) <= target_vector.count(1):
            result_vectors.append(trial_vector)
            result_point_vectors.append(list_of_points_for_trial_vector)
            #print('if')
            #print('is guard set', is_guard_set(list_of_points_for_trial_vector, polygon)[0])
        else:
            result_vectors.append(target_vector)
            #print('else')
            result_point_vectors.append(current_population_with_points[i])
            #print('is guard set', is_guard_set(current_population_with_points[i], polygon)[0])



    return result_point_vectors, result_vectors



def run_de_best_algorithm(filename)->List[point]:
    start_time = time.time()
    p = create_coordinates(filename)
    polygon = Polygon(p)
    init_population = create_init_population(reflex_vertices(polygon), polygon)
    result = de_best_1_bin(init_population[0], init_population[1], polygon)


    final = [result]

    # print('init', final)
    #
    # print(len(result[1]))
    # for i in range(0, len(result[1])):
    #     print(result[1][i].count(1))

    #print('num of reflex', len(reflex_vertices(polygon)))

    guards = []
    h = 30
    for i in range(0, h):

        result1 = de_rand_1_bin(final[i][0], final[i][1], polygon)
        final.append(result1)
        guards = [result1[0]]
    min = 1000
    max = 0
    position = 0
    srednja = 0
    pos_max = 0
    test = 0
    for k in range(0, len(final[h][1])):
        test = len(postprocessing(final[h][0][k], polygon))
        min_k = final[h][1][k].count(1)
        max_k = final[h][1][k].count(1)
        print('mink', min_k)
        # if min > min_k:
        #     min = min_k
        #     position = k
        #     guards = final[h][0][k].copy()
        if min > test:
            min = test
            position = k
        # if max < max_k:
        #     max = max_k
        #     pos_max = k
        if max < test:
            max = test
        srednja = srednja + test


    print("--- %s seconds ---" % (time.time() - start_time))


    print('postprocessing')
    #print(postprocessing(final[h][0][position], polygon))
    #print('final result:', postprocessing(final[h][0][position], polygon))
    print('max guards', max)
    print('srednja ', srednja / len(final[h][1]))
    print('min guards', min)
    return postprocessing(final[h][0][position], polygon)

def draw_segments_best_de(filename):
    p = create_coordinates(filename)
    polygon = Polygon(p)

    result = run_de_best_algorithm(filename)

    return is_guard_set(result, polygon)[1], result




def del_guards(input_l:List[point], poly:Polygon)->List[point]:
    for i in range(0, len(input_l)):
        print('i', i)
        print('len res', len(input_l))
        pom = input_l.copy()
        print('len pom', len(pom))
        del pom[i]
        print('del pom[i]')
        if is_guard_set(pom, poly)[0]:
            del input_l[i]
            print('if')
    return input_l

def visible_points(p:point, poly:Polygon):

        counter = 0
        for vertex in poly.points:
            s = segment(vertex, p)
            # srediste segmenta
            p1 = point((vertex.x + p.x) / 2, (vertex.y + p.y) / 2)
            # potrebno je provjeriti da li je segment unutar poligona sa PointInsidePolygon(p1, poly):

            if not IntersectionP1(poly, s) and PointInsidePolygon(p1, poly):
                counter += 1

            # slucaj kada se segmenti preklapaju, tj kada cuvar sa refleksne ivice vidi susjedni vrh
            else:
                for i in range(0, len(poly.points)):
                    seg = segment(poly.points[i], poly.points[(i + 1) % len(poly.points)])
                    if same_segments(seg, s):
                        counter += 1

        return counter
#
# def postprocessing1(result:List[point], poly:Polygon)-> List[point]:
#
#
#     num_of_visible_points = []
#
#
#     for p in result:
#
#         counter = visible_points(p, poly)
#
#         num_of_visible_points.append([p, counter])
#     print('num of visible points', num_of_visible_points)
#
#     #return num_of_visible_points
#
#     for i in range(0, len(num_of_visible_points)):
#         if num_of_visible_points[i][1] == len(poly.points)-1:
#             return [num_of_visible_points[i][0]]
#
#     guards = []
#     for i in range(0, len(result)):
#         p = visible_points(result[i], poly)
#
#         guards.append([result[i], p])
#     guards = sorted(guards, key=lambda x: x[1])
#     print('guards with num of points they see', guards)
#
#     sorted_result = []
#
#     for i in guards:
#         sorted_result.append(i[0])
#     print('sorted guards', sorted_result)
#
#     # trazimo min broj tacaka koje cuvar vidi i izbacujemo tog cuvara ukoliko je skup, skup cuvara i bez njega
#     # radimo tako, trazeci min broj sve dok mozemo izbaciti nekog od cuvara
#     deleted = True
#     while deleted:
#         print('True section with deleted')
#
#
#
#         pom = result.copy()
#         print('pom', pom)
#         print('result', result)
#         print('num of vis point', num_of_visible_points)
#         print('pom[pos]', pom[pos])
#
#         del pom[pos]
#
#         print('pom/pos', pom)
#
#         if is_guard_set(pom, poly)[0]:
#
#             print('result', result)
#             print('result[pos]', result[pos])
#             del result[pos]
#
#             del num_of_visible_points[pos]
#             print('after deleting result[pos]', result)
#             print('guard set')
#         else:
#             deleted = False
#
#
#     return result
# #
#




# def postprocessing(result:List[point], poly:Polygon)-> List[point]:
#     deleted1 = True
#
#
#     result_pp1 = postprocessing1(result, poly)
#
#     guards = []
#     for i in range(0, len(result_pp1)):
#         p = visible_points(result_pp1[i], poly)
#
#         guards.append([result_pp1[i], p])
#     guards = sorted(guards, key=lambda x: x[1])
#     print('guards with num of points they see', guards)
#
#     sorted_result = []
#
#     for i in guards:
#         sorted_result.append(i[0])
#     print('sorted guars', sorted_result)
#
#     while deleted1:
#         print('true section with deleted1')
#         positions = []
#         for i in range(0, len(sorted_result)):
#             print('i', i)
#             print('len res', len(sorted_result))
#             pom = sorted_result.copy()
#             print('len pom', len(pom))
#             del pom[i]
#             print('del pom[i]')
#             if is_guard_set(pom, poly)[0]:
#                 positions.append(sorted_result[i])
#                 print('positions', positions)
#                 # del result[i]
#                 print('if')
#                 sorted_result = [ele for ele in sorted_result if ele not in positions]
#
#     # if len(positions) == 0:
#         #     deleted1 = False
#         # else:
#
#             # for i in range(0, len(positions)):
#             #     print('i')
#             #     print('result[i]', result[i])
#             #     del result[i]
#
#     return sorted_result



def postprocessing(result:List[point], poly:Polygon)-> List[point]:
    deleted1 = True


    #result_pp1 = postprocessing1(result, poly)

    guards = []
    for i in range(0, len(result)):
        p = visible_points(result[i], poly)

        guards.append([result[i], p])
    guards = sorted(guards, key=lambda x: x[1])
    #print('guards with num of points they see', guards)

    sorted_result = []

    for i in guards:
        sorted_result.append(i[0])
    #print('sorted guars', sorted_result)

    deleted1 = True
    #while deleted1:
    indicator = True
    while indicator:
        #print('true section with deleted1')
        positions = []
        position = 0

        obrisan = False
        while position < len(sorted_result):
           # print('len res', len(sorted_result))
            pom = sorted_result.copy()
            #print('len pom', len(pom))
            del pom[position]
            #print('del pom[i]')
            if is_guard_set(pom, poly)[0]:
                positions.append(sorted_result[position])
                #print('positions', positions)
                del sorted_result[position]
                del guards[position]
                obrisan = True
                #print('if')
                #sorted_result = [ele for ele in sorted_result if ele not in positions]

            else:
                position += 1
        if obrisan is False:
            indicator = False
        #deleted1 = indicator
    # if len(positions) == 0:
        #     deleted1 = False
        # else:

            # for i in range(0, len(positions)):
            #     print('i')
            #     print('result[i]', result[i])
            #     del result[i]
    #print('guards with num of posint', guards)
    #print('sorted result', sorted_result)

    pom_test = sorted_result.copy()

    # for i in range(0, len(sorted_result)):
    #
    #     del pom_test[i]
    #     print(is_guard_set(pom_test, poly)[0], i)
    #     pom_test = sorted_result.copy()
    #print(is_guard_set(sorted_result, poly)[0])

    return sorted_result



print('20-1', run_de_algorithm('randsimple-20-1'))

print('20-2', run_de_algorithm( 'randsimple-20-2'))

print('20-3', run_de_algorithm( 'randsimple-20-3'))

print('20-4', run_de_algorithm( 'randsimple-20-4'))

print('20-5', run_de_algorithm( 'randsimple-20-5'))

print('20-6', run_de_algorithm( 'randsimple-20-6'))

print('20-7', run_de_algorithm( 'randsimple-20-7'))

print('20-8', run_de_algorithm( 'randsimple-20-8'))

print('20-9', run_de_algorithm( 'randsimple-20-9'))

print('20-10', run_de_algorithm( 'randsimple-20-10'))

print('20-11', run_de_algorithm( 'randsimple-20-11'))

print('20-12', run_de_algorithm( 'randsimple-20-12'))

print('20-13', run_de_algorithm( 'randsimple-20-13'))

print('20-14', run_de_algorithm( 'randsimple-20-14'))

print('20-15', run_de_algorithm( 'randsimple-20-15'))

print('20-16', run_de_algorithm( 'randsimple-20-16'))

print('20-17', run_de_algorithm( 'randsimple-20-17'))

print('20-18', run_de_algorithm( 'randsimple-20-18'))

print('20-19', run_de_algorithm( 'randsimple-20-19'))

print('20-80', run_de_algorithm( 'randsimple-20-20'))

print('20-21', run_de_algorithm( 'randsimple-20-21'))

print('20-22', run_de_algorithm( 'randsimple-20-22'))

print('20-23', run_de_algorithm( 'randsimple-20-23'))

print('20-24', run_de_algorithm( 'randsimple-20-24'))

print('20-25', run_de_algorithm( 'randsimple-20-25'))

print('20-26', run_de_algorithm( 'randsimple-20-26'))

print('20-27', run_de_algorithm( 'randsimple-20-27'))

print('20-28', run_de_algorithm( 'randsimple-20-28'))

print('20-29', run_de_algorithm( 'randsimple-20-29'))

print('20-30', run_de_algorithm( 'randsimple-20-30'))


print('40-1', run_de_algorithm( 'randsimple-40-1'))

print('40-2', run_de_algorithm( 'randsimple-40-2'))

print('40-3', run_de_algorithm( 'randsimple-40-3'))

print('40-4', run_de_algorithm( 'randsimple-40-4'))

print('40-5', run_de_algorithm( 'randsimple-40-5'))

print('40-6', run_de_algorithm( 'randsimple-40-6'))

print('40-7', run_de_algorithm( 'randsimple-40-7'))

print('40-8', run_de_algorithm( 'randsimple-40-8'))

print('40-9', run_de_algorithm( 'randsimple-40-9'))

print('40-10', run_de_algorithm( 'randsimple-40-10'))

print('40-11', run_de_algorithm( 'randsimple-40-11'))

print('40-12', run_de_algorithm( 'randsimple-40-12'))

print('40-13', run_de_algorithm( 'randsimple-40-13'))

print('40-14', run_de_algorithm( 'randsimple-40-14'))

print('40-15', run_de_algorithm( 'randsimple-40-15'))

print('40-16', run_de_algorithm( 'randsimple-40-16'))

print('40-17', run_de_algorithm( 'randsimple-40-17'))

print('40-18', run_de_algorithm( 'randsimple-40-18'))

print('40-19', run_de_algorithm( 'randsimple-40-19'))

print('40-20', run_de_algorithm( 'randsimple-40-20'))

print('40-21', run_de_algorithm( 'randsimple-40-21'))

print('40-22', run_de_algorithm( 'randsimple-40-22'))

print('40-23', run_de_algorithm( 'randsimple-40-23'))

print('40-24', run_de_algorithm( 'randsimple-40-24'))

print('40-25', run_de_algorithm( 'randsimple-40-25'))

print('40-26', run_de_algorithm( 'randsimple-40-26'))

print('40-27', run_de_algorithm( 'randsimple-40-27'))

print('40-28', run_de_algorithm( 'randsimple-40-28'))

print('40-29', run_de_algorithm( 'randsimple-40-29'))

print('40-30', run_de_algorithm( 'randsimple-40-30'))

print('60-1', run_de_algorithm( 'randsimple-60-1'))

print('60-2', run_de_algorithm( 'randsimple-60-2'))

print('60-3', run_de_algorithm( 'randsimple-60-3'))

print('60-4', run_de_algorithm( 'randsimple-60-4'))

print('60-5', run_de_algorithm( 'randsimple-60-5'))

print('60-6', run_de_algorithm( 'randsimple-60-6'))

print('60-7', run_de_algorithm( 'randsimple-60-7'))

print('60-8', run_de_algorithm( 'randsimple-60-8'))

print('60-9', run_de_algorithm( 'randsimple-60-9'))

print('60-10', run_de_algorithm( 'randsimple-60-10'))

print('60-11', run_de_algorithm( 'randsimple-60-11'))

print('60-12', run_de_algorithm( 'randsimple-60-12'))

print('60-13', run_de_algorithm( 'randsimple-60-13'))

print('60-14', run_de_algorithm( 'randsimple-60-14'))

print('60-15', run_de_algorithm( 'randsimple-60-15'))

print('60-16', run_de_algorithm( 'randsimple-60-16'))

print('60-17', run_de_algorithm( 'randsimple-60-17'))

print('60-18', run_de_algorithm( 'randsimple-60-18'))

print('60-19', run_de_algorithm( 'randsimple-60-19'))

print('60-80', run_de_algorithm( 'randsimple-60-20'))

print('60-21', run_de_algorithm( 'randsimple-60-21'))

print('60-22', run_de_algorithm( 'randsimple-60-22'))

print('60-23', run_de_algorithm( 'randsimple-60-23'))

print('60-24', run_de_algorithm( 'randsimple-60-24'))

print('60-25', run_de_algorithm( 'randsimple-60-25'))

print('60-26', run_de_algorithm( 'randsimple-60-26'))

print('60-27', run_de_algorithm( 'randsimple-60-27'))

print('60-28', run_de_algorithm( 'randsimple-60-28'))

print('60-29', run_de_algorithm( 'randsimple-60-29'))

print('60-30', run_de_algorithm( 'randsimple-60-30'))

print('80-1', run_de_algorithm( 'randsimple-80-1'))

print('80-2', run_de_algorithm( 'randsimple-80-2'))

print('80-3', run_de_algorithm( 'randsimple-80-3'))

print('80-4', run_de_algorithm( 'randsimple-80-4'))

print('80-5', run_de_algorithm( 'randsimple-80-5'))

print('80-6', run_de_algorithm( 'randsimple-80-6'))

print('80-7', run_de_algorithm( 'randsimple-80-7'))

print('80-8', run_de_algorithm( 'randsimple-80-8'))

print('80-9', run_de_algorithm( 'randsimple-80-9'))

print('80-10', run_de_algorithm( 'randsimple-80-10'))

print('80-11', run_de_algorithm( 'randsimple-80-11'))

print('80-12', run_de_algorithm( 'randsimple-80-12'))

print('80-13', run_de_algorithm( 'randsimple-80-13'))

print('80-14', run_de_algorithm( 'randsimple-80-14'))

print('80-15', run_de_algorithm( 'randsimple-80-15'))

print('80-16', run_de_algorithm( 'randsimple-80-16'))

print('80-17', run_de_algorithm( 'randsimple-80-17'))

print('80-18', run_de_algorithm( 'randsimple-80-18'))

print('80-19', run_de_algorithm( 'randsimple-80-19'))

print('80-80', run_de_algorithm( 'randsimple-80-20'))

print('80-21', run_de_algorithm( 'randsimple-80-21'))

print('80-22', run_de_algorithm( 'randsimple-80-22'))

print('80-23', run_de_algorithm( 'randsimple-80-23'))

print('80-24', run_de_algorithm( 'randsimple-80-24'))

print('80-25', run_de_algorithm( 'randsimple-80-25'))

print('80-26', run_de_algorithm( 'randsimple-80-26'))

print('80-27', run_de_algorithm( 'randsimple-80-27'))

print('80-28', run_de_algorithm('randsimple-80-28'))

print('80-29', run_de_algorithm('randsimple-80-29'))

print('80-30', run_de_algorithm('randsimple-80-30'))


