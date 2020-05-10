from tkinter import *
import time

from master.triangulation import ear_clipping, try_n_times_random_point_random_triangle, \
    try_n_times_center_point_random_triangle, try_n_times_find_vertex_guards_of_random_triangle, \
    triangulation_ear_clipping
from structures.conf import *
from master.naive_algorithm import *
from master.differential_evolution import reflex_vertices, is_guard_set, create_init_population

filename = 'randsimple-20-25'


def translate_coord_from_canvas(x: int, y: int) -> point:
    return point(x - CENTER, -(y - CENTER))

def callback(event):
    canvas = event.widget
    x, y = canvas.canvasx(event.x), canvas.canvasx(event.y)
    point = translate_coord_from_canvas(x, y)
    point.draw(canvas)

root = Tk()

root.title("Art gallery problem")
root.geometry(SCREEN_RESOLUTION)

canvas = Canvas(root, width=CANVAS_DIM, height=CANVAS_DIM)
canvas.grid(row=0, column=0)
canvas.bind("<Button-1>", callback)
#canvas.create_line(0, CENTER, CANVAS_DIM, CENTER, width=1, fill="black")
#canvas.create_line(CENTER, 0, CENTER, CANVAS_DIM, width=1, fill="black")




sidebar = Frame(root, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
sidebar.grid(row=0, column=20)


# n = random.randint(3, 20)
#
# i = 0
# l = []
# while i < n:
#     x = random.randint(-300, 300)
#     y = random.randint(-300,300)
#     l.append(point(x, y))
#     i += 1




def make_simple_polygon() -> None:
    p = create_coordinates(filename)
    polygon = Polygon(get_simple_polygon(p))
    polygon.drawTwo(canvas)
    for point in polygon.points:
        point.drawSec(canvas)
    del p


def naive_heuristic() -> None:
    guards = try_n_times(20, filename)
    for guard in guards:
        guard.drawGuard(canvas)
    del guards


def convex_polygon() -> None:


    n = random.randint(3, 6)

    i = 0
    l = []
    while i < n:
        x = random.randint(-300, 300)
        y = random.randint(-300, 300)
        l.append(point(x, y))
        i += 1

    p = Polygon(get_simple_polygon(l))
    p.drawTwo(canvas)
    print(p.convexPolygon())
    print(n)

def test_triangulation() ->  None:


    #triangles = ear_clipping(filename)
    triangles = triangulation_ear_clipping(filename)

    for t in triangles:
        t.drawSec(canvas)


# bira se slucajna tacka trougla u slucajno odabranom trouglu

def random_point_random_triangle() -> None:
    guards = try_n_times_random_point_random_triangle(100, filename)[0]
    #segments = try_n_times_random_point_random_triangle(100, filename)[1]
    #triangles = ear_clipping(filename)
    #for t in triangles:
        #t.drawSec(canvas)

    for guard in guards:
        guard.drawGuard(canvas)



def center_point_random_triangle() -> None:
    guards = try_n_times_center_point_random_triangle(200, filename)

    #triangles = ear_clipping(filename)
    #for t in triangles:
        #t.drawSec(canvas)
    for guard in guards:
        guard.drawGuard(canvas)

def vertex_point_random_triangle() -> None:
    guards = try_n_times_find_vertex_guards_of_random_triangle(200, filename)

    #guards = find_vertex_guards_of_random_triangle('randsimple-20-25')

    #triangles = ear_clipping(filename)
    #for t in triangles:
        #t.drawSec(canvas)
    for guard in guards:
        guard.drawGuard(canvas)

def reflex_vertices_draw() ->None:
    p = create_coordinates(filename)
    polygon = Polygon(get_simple_polygon(p))
    points = reflex_vertices(polygon)
    for point in points:
        point.drawReflex(canvas)
    rez = points
    result = is_guard_set(points, polygon)
    for s in result[1]:
        s.drawSeg(canvas)
    print(result[0])


def create_init_population_draw()-> None:
    p = create_coordinates(filename)
    polygon = Polygon(get_simple_polygon(p))
    points = reflex_vertices(polygon)
    result = create_init_population(points, polygon)[0]
    result1 = is_guard_set(result[0], polygon)
    print('guard set', result1[0])
    guards = result[5]
    for g in guards:
        g.drawGuard(canvas)

    for s in result1[1]:
        s.drawSeg(canvas)

def clear() -> None:
    canvas.delete("all")
    ##canvas.create_line(CENTER, 0, CENTER, CANVAS_DIM, width=1, fill="black")



Button(sidebar, text='Make simple polygon',
       command=make_simple_polygon, padx=30, pady=5).grid(row=2, column=5)
#Frame(sidebar, height=5).grid(row=3, column=1)

Button(sidebar, text='Naive heuristic',
       command=naive_heuristic, padx=30, pady=5).grid(row=8, column=5)
#Frame(sidebar, height=5).grid(row=9, column=1)




Button(sidebar, text='random_point_random_triangle',
       command=random_point_random_triangle, padx=30, pady=5).grid(row=15, column=5)
#Frame(sidebar, height=5).grid(row=13, column=1)



Button(sidebar, text='center_point_random_triangle',
       command=center_point_random_triangle, padx=30, pady=5).grid(row=20, column=5)
#Frame(sidebar, height=5).grid(row=13, column=1)



Button(sidebar, text='vertex_point_random_triangle',
       command=vertex_point_random_triangle, padx=30, pady=2).grid(row=25, column=5)
#Frame(sidebar, height=5).grid(row=13, column=1)




#---------------------------------------------


Button(sidebar, text='reflex vertices',
       command=reflex_vertices_draw, padx=30, pady=5).grid(row=30, column=5)
#Frame(sidebar, height=5).grid(row=13, column=1)

Button(sidebar, text='triangulation',
       command=test_triangulation, padx=30, pady=5).grid(row=40, column=5)
#Frame(sidebar, height=5).grid(row=13, column=1)




Button(sidebar, text='init',
       command=create_init_population_draw, padx=50, pady=5).grid(row=50, column=5)

Button(sidebar, text='Clear',
       command=clear, padx=50, pady=5).grid(row=60, column=5)


root.mainloop()

