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
            x= int(slope * y)
            self.set_pixel(x,y, **kargs)
            
    def display(self):
        print("\n".join(["".join(row) for row in self.data]))


import math

class Shape:
    def __init__(self, x, y):
        self._x = x
        self._y = y
    
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
        canvas.h_line(self._x, self._y+self.width, self.height, char=char)
        # vertical lines
        canvas.v_line(self._x, self._y, self.height, char=char) 
        canvas.v_line(self._x+self.height, self._y, self.width, char=char)


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

class Triangle(Shape):
    def __init__(self, x, y, base, height):
        super().__init__(x, y)
        self.base = base
        self.height = height
        self.vertices = [(x, y), (x + base, y), (x + base / 2, y + height)]  # Simplified for equilateral triangles
    
    def area(self):
        return 0.5 * self.base * self.height
    
    def perimeter(self):
        return 3 * self.base  # Assuming an equilateral triangle for simplicity

    def get_perimeter_points(self):
        return self.vertices
    
    def is_inside(self, x_point, y_point):
        # Vertices of the triangle
        x1, y1 = self.vertices[0]
        x2, y2 = self.vertices[1]
        x3, y3 = self.vertices[2]
        
        # Area of the main triangle (ABC)
        area_ABC = abs(x1*(y2 - y3) + x2*(y3 - y1) + x3*(y1 - y2)) / 2.0
        
        # Areas of the sub-triangles formed with the point (P)
        area_PAB = abs(x_point*(y1 - y2) + x1*(y2 - y_point) + x2*(y_point - y1)) / 2.0
        area_PBC = abs(x_point*(y2 - y3) + x2*(y3 - y_point) + x3*(y_point - y2)) / 2.0
        area_PCA = abs(x_point*(y3 - y1) + x3*(y1 - y_point) + x1*(y_point - y3)) / 2.0
        
        # If the sum of the areas of the sub-triangles is equal to the area of the triangle, the point is inside
        return area_ABC == area_PAB + area_PBC + area_PCA
        
    def paint(self, canvas, char='*'):
        x1, y1 = self.vertices[0]
        x2, y2 = self.vertices[1]
        x3, y3 = self.vertices[2]
        canvas.line(x1, y1, x2, y2)
        canvas.line(x1, y1, x3, y3)
        canvas.line(x2,y2, x3, y3)