class Canvas:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # Empty canvas is a matrix with element being the "space" character
        self.data = [[' '] * width for i in range(height)]

    def set_pixel(self, row, col, char='*'):
        self.data[row][col] = char

    def get_pixel(self, row, col):
        return self.data[row][col]
    
    def clear_canvas(self):
        self.data = [[' '] * self.width for i in range(self.height)]
    
    def v_line(self, x, y, w, **kargs):
        for i in range(x,x+w):
            self.set_pixel(i,y, **kargs)

    def h_line(self, x, y, h, **kargs):
        for i in range(y,y+h):
            self.set_pixel(x,i, **kargs)
            
    def line(self, x1, y1, x2, y2, **kargs):
        slope = (y2-y1) / (x2-x1)
        for y in range(y1,y2):
            x = int(slope * y)
            self.set_pixel(x,y, **kargs)
            
    def display(self):
        print("\n".join(["".join(row) for row in self.data]))


import math

class Shape:
    def __init__(self, x, y):
        self._x = x
        self._y = y
        self.name=""
    
    def get_x(self):
        return self._x
    
    def get_y(self):
        return self._y
    
    def area(self):
        raise NotImplementedError("Subclasses must implement this method")
    
    def perimeter(self):
        raise NotImplementedError("Subclasses must implement this method")
    
    def get_perimeter_points(self):
        raise NotImplementedError("Subclasses must implement this method")

    def is_inside(self, x_point, y_point):
        raise NotImplementedError("Subclasses must implement this method")
        
    def is_overlap(self, other):
        if isinstance(other, Shape):
            if isinstance(self, Rectangle) and isinstance(other, Rectangle):
                return self._overlap_with_rectangle(other)
            elif isinstance(self, Circle) and isinstance(other, Circle):
                return self._overlap_with_circle(other)
            elif isinstance(self, Triangle) and isinstance(other, Triangle):
                return self._overlap_with_triangle(other)
        return False
    
    def _overlap_with_rectangle(self, other):
        return not (self._x + self.width < other._x or
                    self._x > other._x + other.width or
                    self._y + self.height < other._y or
                    self._y > other._y + other.height)
    
    def _overlap_with_circle(self, other):
        distance = math.sqrt((self._x - other._x) ** 2 + (self._y - other._y) ** 2)
        return distance < (self.radius + other.radius)
    
    def _overlap_with_triangle(self, other):
        return (self.is_inside(other._x, other._y) or
                other.is_inside(self._x, self._y))


# Rectangle Class
class Rectangle(Shape):
    def __init__(self, x, y, width, height):
        super().__init__(x, y)
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height
    
    def perimeter(self):
        return 2 * (self.width + self.height)

    def get_perimeter_points(self):
        return [(self._x, self._y), (self._x + self.width, self._y),
                (self._x + self.width, self._y + self.height), (self._x, self._y + self.height)]
    
    def is_inside(self, x_point, y_point):
        return self._x <= x_point <= self._x + self.width and self._y <= y_point <= self._y + self.height
        
    def paint(self, canvas, char='*'):
        # horizontal lines
        canvas.h_line(self._x, self._y, self.height, char=char)
        canvas.h_line(self._x+self.width, self._y, self.height, char=char)

        # vertical lines
        canvas.v_line(self._x, self._y, self.height, char=char) 
        canvas.v_line(self._x, self._y+self.height, self.width, char=char)

    def __repr__(self):
        return "Rectangle ("+repr(self._x)+","+repr(self._y)+","+repr(self.width)+","+repr(self.height)+") "


# Circle Class
class Circle(Shape):
    def __init__(self, x, y, radius):
        super().__init__(x, y)
        self.radius = radius
    
    def area(self):
        return math.pi * (self.radius ** 2)
    
    def perimeter(self):
        return 2 * math.pi * self.radius

    def get_perimeter_points(self):
        return [(self._x + self.radius, self._y), (self._x - self.radius, self._y),
                (self._x, self._y + self.radius), (self._x, self._y - self.radius)]
    
    def is_inside(self, x_point, y_point):
        distance = math.sqrt((x_point - self._x) ** 2 + (y_point - self._y) ** 2)
        return distance < self.radius
        
    def paint(self, canvas, char='*'):
        for angle in range(0, 360, 15):
            rad=math.radians(angle)
            x=int(self._x+self.radius*math.cos(rad))
            y=int(self._y+self.radius*math.sin(rad))

            if 0<=x<canvas.width and 0<=y<canvas.height:
                canvas.set_pixel(y, x, char)

    def __repr__(self):
        return "Circle ("+repr(self._x)+","+repr(self._y)+","+repr(self.radius)+") "

class Triangle(Shape):
    def __init__(self, side1, side2, side3, x, y):
        super().__init__(x, y)
        self.__side1 = side1
        self.__side2 = side2
        self.__side3 = side3
    
    def get_sides(self):
        return self.__side1, self.__side2, self.__side3
    
    def area(self):
        s = (self.__side1 + self.__side2 + self.__side3) / 2
        return math.sqrt(s * (s - self.__side1) * (s - self.__side2) * (s - self.__side3))
    
    def perimeter(self):
        return self.__side1 + self.__side2 + self.__side3
    
    def get_perimeter_points(self):
        points = []
        
        for i in range(5):
            x_point = self._x + (self.__side1 / 4) * i
            y_point = self._y
            points.append((x_point, y_point))
        
        for i in range(5):
            x_point = self._x + (self.__side2 / 4) * i
            y_point = self._y + (self.__side3 / 4) * i
            points.append((x_point, y_point))
        
        for i in range(5):
            x_point = self._x + self.__side2
            y_point = self._y + (self.__side3 / 4) * i
            points.append((x_point, y_point))
        
        return points
    
    def is_inside(self, x, y):
        def sign(p1, p2, p3):
            return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])
        
        p1 = (self._x, self._y)
        p2 = (self._x + self.__side1, self._y)
        p3 = (self._x + self.__side2 / 2, self._y + math.sqrt(self.__side3**2 - (self.__side2 / 2)**2))
        
        d1 = sign((x, y), p1, p2)
        d2 = sign((x, y), p2, p3)
        d3 = sign((x, y), p3, p1)
        
        has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
        has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
        
        return not (has_neg and has_pos)
        
    def paint(self, canvas, char='*'):
        for point in self.get_perimeter_points():
            canvas.set_pixel(int(point[0]), int(point[1]))

    def __repr__(self):
        return "Triangle ("+repr(self.__side1)+","+repr(self.__side2)+","+repr(self.__side3)+","+repr(self._x)+","+repr(self._y)+") "