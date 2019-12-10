class Quad:
    def __init__(self, canvas, x, y, width):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.width = width
        self.points = []
        self.children = []
        self.max_points = 4
        self.min_width = 2
        self.divided = False
        self.display()

    def display(self):
        self.canvas.create_line((self.x, self.y, self.x + self.width, self.y), fill = "#646464")
        self.canvas.create_line((self.x, self.y, self.x, self.y + self.width), fill = "#646464")
        self.canvas.create_line((self.x + self.width, self.y, self.x + self.width, self.y + self.width), fill = "#646464")
        self.canvas.create_line((self.x, self.y + self.width, self.x + self.width, self.y + self.width), fill = "#646464")

    def add_points(self, points):
        if self.divided:
            for child in self.children:
                child.add_points(points)
        else:
            for point in points:
                #  If point is in self
                if self.x < point.x <= self.x + self.width and self.y < point.y <= self.y + self.width:
                    self.points.append(point)
            self.check_points()

    def divide(self):
        self.divided = True
        #  Create 4 smaller children quads inside self
        self.children.append(Quad(self.canvas, self.x, self.y, self.width / 2))
        self.children.append(Quad(self.canvas, self.x + self.width / 2, self.y, self.width / 2))
        self.children.append(Quad(self.canvas, self.x, self.y + self.width / 2, self.width / 2))
        self.children.append(Quad(self.canvas, self.x + self.width / 2, self.y + self.width / 2, self.width / 2))
        #  Move points from self to children
        for child in self.children:
            child.add_points(self.points)
        self.points.clear()

    def check_points(self):
        if len(self.points) > self.max_points and self.width > self.min_width:
            self.divide()

    def find_points(self, rectangle):
        points_in_rectangle = []
        #  Check if rectangle intersects self
        if not(rectangle.min_x > self.x + self.width or rectangle.max_x < self.x or rectangle.min_y > self.y + self.width or rectangle.max_y < self.y):
            if self.divided:
                for child in self.children:
                    points_in_rectangle += child.find_points(rectangle)
            else:
                for point in self.points:
                    #  Check if point is in rectangle
                    if rectangle.min_x < point.x < rectangle.max_x and rectangle.min_y < point.y < rectangle.max_y:
                        points_in_rectangle.append(point)

        return points_in_rectangle


class Point:
    def __init__(self, canvas, x, y, colour):
        self.x = x
        self.y = y
        self.display = canvas.create_oval(x - 2, y - 2, x + 2, y + 2, outline = colour, fill = colour)


class Rectangle:
    def __init__(self, canvas, x1, y1, x2, y2):
        self.min_x = min(x1, x2)
        self.min_y = min(y1, y2)
        self.max_x = max(x1, x2)
        self.max_y = max(y1, y2)
        self.display = canvas.create_rectangle((x1, y1, x2, y2), outline = "white")
