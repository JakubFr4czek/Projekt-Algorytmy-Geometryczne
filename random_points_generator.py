import random as rd
import math as mth
from geometry import Circle, Rectangle

class Random:

    @staticmethod
    def generate_uniform_points(n=100, min_x = -100, max_x = 100, min_y = -100, max_y = 100):

        T = []

        for i in range( n ):

            T.append((rd.uniform(min_x, max_x), rd.uniform(min_y, max_y)))
            
        return T

    @staticmethod
    def generate_circle_points(n=100, circle = Circle((0, 0), 100)):
        
        T = []
        
        for i in range(n):

            f = rd.uniform(0, 2) * mth.pi

            x = circle.r * mth.cos(f) - circle.S[0]
            y = circle.r * mth.sin(f) - circle.S[1]

            T.append((x,y))
            
        return T

    @staticmethod
    def generate_rectangle_points(n=100, rectangle = Rectangle((-10, 10), (10, 10), (10, -10), (-10, -10))):

        T = []

        a = rectangle.vertices[0]
        b = rectangle.vertices[1]
        c = rectangle.vertices[2]
        d = rectangle.vertices[3]

        v1 = (a[0] - b[0], a[1] - b[1])
        v2 = (b[0] - c[0], b[1] - c[1])
        v3 = (c[0] - d[0], c[1] - d[1])
        v4 = (d[0] - a[0], d[1] - a[1])

        for i in range(n):
            x = rd.randint(1, 4)
            y = rd.random()

            if x ==1:
                T.append( (b[0] + v1[0] * y, b[1] + v1[1] * y) )
            elif x == 2:
                T.append( (c[0] + v2[0] * y, c[1] + v2[1] * y) )
            elif x == 3:
                T.append( (d[0] + v3[0] * y, d[1] + v3[1] * y) )
            else:
                T.append( (a[0] + v4[0] * y, a[1] + v4[1] * y) )
        
        return T

"""
def generate_square_points(a=(0, 0), b=(10, 0), c=(10, 10), d=(0, 10), axis_n=25, diag_n=20):

    T = []

    v1 = (a[0] - b[0], a[1] - b[1])
    v2 = (d[0] - a[0], d[1] - a[1])

    for i in range(axis_n):
        
        y = rd.random()
        
        T.append( (b[0] + v1[0] * y, b[1] + v1[1] * y) )
        
    for i in range(axis_n):

        y = rd.random()
    
        T.append( (a[0] + v2[0] * y, a[1] + v2[1] * y) )

    d1 = (b[0] - d[0], b[1] - d[1])
    d2 = (a[0] - c[0], a[1] - c[1])
    
    for i in range(diag_n):

        y = rd.random()

        T.append( (d[0] + d1[0] * y, d[1] + d1[1] * y) )

    for i in range(diag_n):

        y = rd.random()

        T.append( (c[0] + d2[0] * y, c[1] + d2[1] * y) )

    return T
"""