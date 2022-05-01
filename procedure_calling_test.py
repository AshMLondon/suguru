#procedure calling test
#just checking if i can call procedures from other files ok

import gridgenerate

print ("procedure calling test")

#let's start with the random colour one which has no inputs
#from gridgenerate  import random_colour, gen_predet_shapes, translated_shapes
from gridgenerate import *

print (random_colour())

#now let's try generating a grid
#global initial variables
gridgenerate.num_rows=6
gridgenerate.num_cols=6
gridgenerate.verbose=False
gridgenerate.display_build=False


# grid = np.zeros((gridgenerate.num_rows, gridgenerate.num_cols), dtype=int)
# grid_shapes = np.zeros((gridgenerate.num_rows, gridgenerate.num_cols), dtype=int)

create_blank_grids()
gen_predet_shapes(turtle_fill=False)

print(gridgenerate.grid_shapes)
