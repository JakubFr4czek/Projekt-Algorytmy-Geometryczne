import time
import sys
from random_points_generator import Random
from mbr import Mbr
from convexhull import Graham

sys.setrecursionlimit(100_000_000)

points_n_100 = Random.generate_uniform_points(n = 100)
points_n_1_000 = Random.generate_uniform_points(n = 1_000)
points_n_10_000 = Random.generate_uniform_points(n = 10_000)
points_n_100_000 = Random.generate_uniform_points(n = 100_000)
points_n_1_000_000 = Random.generate_uniform_points(n = 1_000_000)

start = time.time()
Mbr.smallest_rectangle(points_n_100, compare=Mbr.compare_area)
print("Random uniform dla n = 100: ", time.time() - start)

start = time.time()
Mbr.smallest_rectangle(points_n_1_000, compare=Mbr.compare_area)
print("Random uniform dla n = 1_000: ", time.time() - start)

start = time.time()
Mbr.smallest_rectangle(points_n_10_000, compare=Mbr.compare_area)
print("Random uniform dla n = 10_000: ", time.time() - start)

start = time.time()
Mbr.smallest_rectangle(points_n_100_000, compare=Mbr.compare_area)
print("Random uniform dla n = 100_000: ", time.time() - start)

start = time.time()
Mbr.smallest_rectangle(points_n_1_000_000, compare=Mbr.compare_area)
print("Random uniform dla n = 1_000_000: ", time.time() - start)

points_circle_n_100 = Random.generate_circle_points(n = 100)
points_circle_n_1_000 = Random.generate_circle_points(n = 1_000)
points_circle_n_10_000 = Random.generate_circle_points(n = 10_000)
points_circle_n_100_000 = Random.generate_circle_points(n = 100_000)
points_circle_n_1_000_000 = Random.generate_circle_points(n = 1_000_000)


start = time.time()
Graham.graham_algorithm(points_circle_n_100)
print("Graham dla n = 50: ", time.time() - start)

start = time.time()
Graham.graham_algorithm(points_circle_n_1_000)
print("Graham dla n = 1_000: ", time.time() - start)
0
start = time.time()
Graham.graham_algorithm(points_circle_n_10_000)
print("Graham dla n = 10_000: ", time.time() - start)

start = time.time()
Graham.graham_algorithm(points_circle_n_100_000)
print("Graham dla n = 100_000: ", time.time() - start)

start = time.time()
Graham.graham_algorithm(points_circle_n_1_000_000)
print("Graham dla n = 1_000_000: ", time.time() - start)


start = time.time()
Mbr.smallest_rectangle(points_circle_n_100, compare=Mbr.compare_area)
print("Circle dla n = 100: ", time.time() - start)

start = time.time()
Mbr.smallest_rectangle(points_circle_n_1_000, compare=Mbr.compare_area)
print("Circle dla n = 1_000: ", time.time() - start)
0
start = time.time()
Mbr.smallest_rectangle(points_circle_n_10_000, compare=Mbr.compare_area)
print("Circle dla n = 10_000: ", time.time() - start)

#start = time.time()
#Mbr.smallest_rectangle(points_circle_n_100_000, compare=Mbr.compare_area)
#print("Circle dla n = 100_000: ", time.time() - start)

#start = time.time()
#Mbr.smallest_rectangle(points_circle_n_1_000_000, compare=Mbr.compare_area)
#print("Circle dla n = 1_000_000: ", time.time() - start)

points_rectangle_n_100 = Random.generate_rectangle_points(n = 100)
points_rectangle_n_1_000 = Random.generate_rectangle_points(n = 1_000)
points_rectangle_n_10_000 = Random.generate_rectangle_points(n = 10_000)
points_rectangle_n_100_000 = Random.generate_rectangle_points(n = 100_000)
points_rectangle_n_1_000_000 = Random.generate_rectangle_points(n = 1_000_000)


start = time.time()
Mbr.smallest_rectangle(points_rectangle_n_100, compare=Mbr.compare_area)
print("Rectangle dla n = 50: ", time.time() - start)

start = time.time()
Mbr.smallest_rectangle(points_rectangle_n_1_000, compare=Mbr.compare_area)
print("Rectangle dla n = 1_000: ", time.time() - start)
0
start = time.time()
Mbr.smallest_rectangle(points_rectangle_n_10_000, compare=Mbr.compare_area)
print("Rectangle dla n = 10_000: ", time.time() - start)

start = time.time()
Mbr.smallest_rectangle(points_rectangle_n_100_000, compare=Mbr.compare_area)
print("Rectangle dla n = 100_000: ", time.time() - start)

start = time.time()
Mbr.smallest_rectangle(points_rectangle_n_1_000_000, compare=Mbr.compare_area)
print("Rectangle dla n = 1_000_000: ", time.time() - start)





