#puzzle timing test
#let's eee how fast the new puzzle approach works

from puzzle import Puzzle
import time, random
import sys

print (sys.version)

sizes=[(8,5), (9,6), (10,7), (10,8)]

for size in sizes:
    print ("SIZE",size)
    start_time=time.time()
    puzzle = Puzzle(*size)
    puzzle.generate_grid_shapes()
    puzzle.dump_shapes()
    print (f"time to generate grid {round(time.time()-start_time,3)}")
    puzzle.brute_force_solve()
    print (f"time to solution {round(time.time()-start_time,3)}")
    puzzle.dump_solution()

