#try to see time difference between 2D List and Numpy Array

import time
import gridgenerate as gridgen
#import numpy as np

gridgen.create_shape_permutations_and_save_to_file()

exit()





cols=16
rows=8
times_to_run=55000



#First Lists

time_started = time.time()
for runs in range(times_to_run):

    grid_list=[[0 for c in range (cols)] for r in range(rows)]
    count=0
    for r in range(rows):
        for c in range(cols):
            grid_list[r][c]=count+1
            count=(count+1)%5
    #print (grid_list)

    for count in range(5):
        for r in range(rows):
            for c in range(cols):
                if grid_list[r][c]==count+1:
                    grid_list[r][c]=count
        #print (grid_list)

print (f"LISTS Total time {time.time()-time_started}")



#Now Arrays

time_started = time.time()
for runs in range(times_to_run):

    grid_array=np.zeros((rows, cols),dtype=int)
    count=0
    for r in range(rows):
        for c in range(cols):
            grid_array[r,c]=count+1
            count=(count+1)%5
    #print (grid_array)

    for count in range(5):
        for r in range(rows):
            for c in range(cols):
                if grid_array[r,c]==count+1:
                    grid_array[r,c]=count
        #print (grid_array)

print (f"ARRAYS Total time {time.time()-time_started}")

