import random as rd
from geometry import Circle
from bitalg.visualizer.main import Visualizer

class Welzl:

    def __distance_between_points(A, B):

        C = (B[0] - A[0], B[1] - A[1])

        return (C[0]**(2.0) + C[1]**(2.0))**(0.5)

    def __center(A, B, C):
        (x1, y1), (x2, y2), (x3, y3) = A, B, C
        A = x1 * (y2 - y3) - y1 * (x2 - x3) + x2 * y3 - x3 * y2
        B = (x1 ** 2 + y1 ** 2) * (y3 - y2) + (x2 ** 2 + y2 ** 2) * (y1 - y3) + (x3 ** 2 + y3 ** 2) * (y2 - y1)
        C = (x1 ** 2 + y1 ** 2) * (x2 - x3) + (x2 ** 2 + y2 ** 2) * (x3 - x1) + (x3 ** 2 + y3 ** 2) * (x1 - x2)
        return (-B / A / 2, -C / A / 2)

    @classmethod
    def __construct_circle(self, R):

        if len(R) == 0:
            return Circle((0, 0), 0)
        elif len(R) == 1:
            return Circle(R[0], 0)
        elif len(R) == 2:
            
            A = R[0]
            B = R[1]

            S = ( ((A[0] + B[0]) / 2.0), ((A[1] + B[1]) / 2.0) )
            
            r = self.__distance_between_points(A, S)

            return Circle(S, r)
        
        elif len(R) == 3:

            A = R[0]
            B = R[1]
            C = R[2]

            c1 = self.__construct_circle([A, B])
    
            if(self.__in_circle(c1, C)): return c1
                
            c2 = self.__construct_circle([A, C])

            if(self.__in_circle(c2, B)): return c2

            c3 = self.__construct_circle([B, C])

            if(self.__in_circle(c3, A)): return c3


            S = self.__center(A, B, C)

            r = self.__distance_between_points(A, S)

            return Circle(S, r)
        else:
            raise Exception("Wrong \"R\" list size!")

    @classmethod
    def __in_circle(self, circle, point, eps = 10**(-10)):
        #print(distance_between_points(circle.S, point) <= circle.r)
        return self.__distance_between_points(circle.S, point) <= circle.r + eps

    @classmethod
    def welzl_algorithm(self, points):
        return self.__r_welzl_algorithm(points, [], len(points))

    @classmethod
    def __r_welzl_algorithm(self, P, R, last):

        if last == 0 or len(R) == 3:
            return self.__construct_circle(R)
        
        #Wybieram losowo kolejny punkt
        idx = rd.randint(0, last - 1)
        point = P[idx]

        #Zamieniam point z ostatnim elementem w P
        P[idx], P[last-1] = P[last-1], P[idx]
        
        #Biorę okrąg zawierający wszystkie punkty poza point
        circle = self.__r_welzl_algorithm(P, R.copy(), last - 1)

        #Sprawdzam, czy point zawiera się w circle
        if(self.__in_circle(circle, point)):
            #Jeśli tak, to zwracam okrąg
            return circle
        else:
            #Jeśli nie, to point należy do brzegu szukanego okręgu
            R.append(point)

            return self.__r_welzl_algorithm(P, R.copy(), last - 1)
        
    @classmethod
    def welzl_algorithm_draw(self, points, vis = Visualizer()):
        return self.__r_welzl_algorithm_draw(points, [], len(points), vis)

    @classmethod
    def __r_welzl_algorithm_draw(self, P, R, last, vis = Visualizer()):

        if last == 0 or len(R) == 3:
            return self.__construct_circle(R)
        
        #Wybieram losowo kolejny punkt
        idx = rd.randint(0, last - 1)
        point = P[idx]


        #Zamieniam point z ostatnim elementem w P
        P[idx], P[last-1] = P[last-1], P[idx]

        visPoint = vis.add_point(point, color = 'red')

        #Biorę okrąg zawierający wszystkie punkty poza point
        circle = self.__r_welzl_algorithm_draw(P, R.copy(), last - 1, vis)

        visCircle = vis.add_circle((circle.S[0], circle.S[1] , circle.r), color = "green")

        vis.remove_figure(visPoint)

        vis.remove_figure(vis.add_point(point, color = 'black'))

        vis.remove_figure(visCircle)

        #Sprawdzam, czy point zawiera się w circle
        if(self.__in_circle(circle, point)):
            #Jeśli tak, to zwracam okrąg
            return circle
        else:
            #Jeśli nie, to point należy do brzegu szukanego okręgu
            R.append(point)
            

            return self.__r_welzl_algorithm_draw(P, R.copy(), last - 1, vis)