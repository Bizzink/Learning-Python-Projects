from tkinter import Tk, Canvas
from Quad import *
from random import randint

def add_point(mouse):
    global Q, canvas
    points = []  # has do be done this way due to how Quad.add_points() works
    point = Point(canvas, mouse.x, mouse.y, "white")
    points.append(point)
    Q.add_points(points)


def select_rectangle(mouse):
    global temp_x, temp_y, started, Q, canvas
    if started:
        rect = Rectangle(canvas, temp_x, temp_y, mouse.x, mouse.y)
        points = Q.find_points(rect)

        for point in points:
            canvas.itemconfigure(point.display, outline = "green", fill = "green")
        
        canvas.update()
        started = False
    else:
        temp_x = mouse.x
        temp_y = mouse.y
        started = True


def generate_points(count):
    points = []
    for i in range(count):
        point = Point(canvas, randint(0, 700), randint(0, 700), "white")
        points.append(point)

    Q.add_points(points)


root = Tk()
root.title("QuadTree")
canvas = Canvas(root, width=700, height=700, background="#333333")
canvas.pack()
canvas.bind("<Button-1>", select_rectangle)
canvas.bind("<Button-3>", add_point)

started = False
Q = Quad(canvas, 0, 0, 700)

root.after(0, generate_points(1000))
root.mainloop()
