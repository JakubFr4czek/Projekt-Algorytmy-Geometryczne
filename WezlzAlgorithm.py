import random as rd

class Circle:

    def __init__(self, S, r):
        self.S = S
        self.r = r

def distance_between_points(A, B):

    C = (B[0] - A[0], B[1] - A[1])

    return (C[0]**(2.0) + C[1]**(2.0))**(0.5)

def center(A, B, C):
    (x1, y1), (x2, y2), (x3, y3) = A, B, C
    A = x1 * (y2 - y3) - y1 * (x2 - x3) + x2 * y3 - x3 * y2
    B = (x1 ** 2 + y1 ** 2) * (y3 - y2) + (x2 ** 2 + y2 ** 2) * (y1 - y3) + (x3 ** 2 + y3 ** 2) * (y2 - y1)
    C = (x1 ** 2 + y1 ** 2) * (x2 - x3) + (x2 ** 2 + y2 ** 2) * (x3 - x1) + (x3 ** 2 + y3 ** 2) * (x1 - x2)
    return (-B / A / 2, -C / A / 2)

def construct_circle(R):

    if len(R) == 0:
        return Circle((0, 0), 0)
    elif len(R) == 1:
        return Circle(R[0], 0)
    elif len(R) == 2:
        
        A = R[0]
        B = R[1]

        S = ( ((A[0] + B[0]) / 2.0), ((A[1] + B[1]) / 2.0) )
        
        r = distance_between_points(A, S)

        return Circle(S, r)
    
    elif len(R) == 3:

        A = R[0]
        B = R[1]
        C = R[2]

        c1 = construct_circle([A, B])
 
        if(in_circle(c1, C)): return c1
            
        c2 = construct_circle([A, C])

        if(in_circle(c2, B)): return c2

        c3 = construct_circle([B, C])

        if(in_circle(c3, A)): return c3


        S = center(A, B, C)

        r = distance_between_points(A, S)

        return Circle(S, r)
    else:
        raise Exception("Wrong \"R\" list size!")

def in_circle(circle, point):
    #print(distance_between_points(circle.S, point) <= circle.r)
    return distance_between_points(circle.S, point) <= circle.r + 10**(-10)


def welzl_algorithm(P, R, last):

    if last == 0 or len(R) == 3:
        return construct_circle(R)
    
    #Wybieram losowo kolejny punkt
    idx = rd.randint(0, last - 1)
    point = P[idx]

    #Zamieniam point z ostatnim elementem w P
    P[idx], P[last-1] = P[last-1], P[idx]
    
    #Biorę okrąg zawierający wszystkie punkty poza point
    circle = welzl_algorithm(P, R.copy(), last - 1)

    #Sprawdzam, czy point zawiera się w circle
    if(in_circle(circle, point)):
        #Jeśli tak, to zwracam okrąg
        return circle
    else:
        #Jeśli nie, to point należy do brzegu szukanego okręgu
        R.append(point)

        return welzl_algorithm(P, R.copy(), last - 1)