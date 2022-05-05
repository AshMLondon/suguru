#procedure calling test
#just checking if i can call procedures from other files ok

import gridgenerate as gridgen
from time import time


def main():
    print ("procedure calling test")

    #let's start with the random colour one which has no inputs
    #from gridgen  import random_colour, gen_predet_shapes, translated_shapes


    print (gridgen.random_colour())

    #now let's try generating a grid
    #global initial variables
    gridgen.num_rows=10
    gridgen.num_cols=10
    gridgen.verbose=False
    gridgen.display_build=False


    # grid = np.zeros((gridgen.num_rows, gridgen.num_cols), dtype=int)
    # grid_shapes = np.zeros((gridgen.num_rows, gridgen.num_cols), dtype=int)

    start_time=time()

    for loop in range(1):
        gridgen.create_blank_grids()
        gridgen.gen_predet_shapes(turtle_fill=False)

    elapsed= time()-start_time

    print(gridgen.grid_shapes)
    print ("elapsed = ",elapsed)








if __name__ == '__main__':
    main()
