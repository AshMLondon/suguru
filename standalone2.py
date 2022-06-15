import gridgenerate as gridgen
import database_functions as db
import numpy as np
from time import time
import requests, pprint


def solve_via_api(grid_to_try, max_iters=None):
    '''
    function to call the api on heroku to get a faster response using pypy
    :param grid_shapes:
    :return:
    '''
    params={"grid_shapes":grid_to_try.tolist()}  #convert np.array to list
    if max_iters:
        params["max_iters"]=max_iters
    #url_send="http://127.0.0.1:5000/solve_grid_api"
    url_send="https://sugurupypy.herokuapp.com/solve_grid_api"
    response = requests.post(url_send, json=params)
    json_back=response.json()
    #pprint.pprint (json_back)
    #print (json_back.get("grid_values"))
    return json_back



def gen_multi_grids_getstats():
    #generate multiple grids and get stats on how many goes it took

    #global initial variables
    gridgen.num_rows=5
    gridgen.num_cols=7
    gridgen.verbose=False
    gridgen.display_build=False


    # num_success=0
    # num_timeout=0
    counts=[]
    gridgen.max_iters = 1e6
    number_to_loop=1
    for loop in range(number_to_loop):
        start_time = time()
        gridgen.create_blank_grids()
        gridgen.gen_predet_shapes(turtle_fill=False)

        gridgen.shape_coords = gridgen.get_shape_coords()

        gridgen.iterate_cell_count = 0
        gridgen.iterate_number_count = 0

        gridgen.create_iterate_lookups()
        success, timedout = gridgen.real_iterate()
        elapsed= round(time()-start_time,2)

        print (f"#{loop}, cells iterated {gridgen.iterate_cell_count:,}  success? {success}, timedout? {timedout},   time {elapsed}")
        counts.append(gridgen.iterate_cell_count)

        start_time = time()
        print(gridgen.row_col)
        gridgen.row_col={}
        grid_to_reuse=gridgen.grid_shapes.copy()
        gridgen.create_blank_grids()
        spiral_coords=[]
        start_coord=(2,3)
        new_coord=start_coord
        keep_spiraling=True
        counter=0

        while keep_spiraling:
            new_coord=gridgen.next_free_space_spiral(new_coord)
            print(new_coord)
            if new_coord:
                spiral_coords.append(new_coord)
                gridgen.grid_shapes[new_coord]=99
                gridgen.row_col[counter]=new_coord
                counter+=1
            else:
                keep_spiraling=False
        print (len(spiral_coords), spiral_coords)
        print (gridgen.row_col)
        gridgen.grid_shapes=grid_to_reuse.copy()
        print (gridgen.grid_shapes)

        success, timedout = gridgen.real_iterate()
        elapsed = round(time() - start_time, 2)
        print(f"V2S #{loop}, cells iterated {gridgen.iterate_cell_count:,}  success? {success}, timedout? {timedout},   time {elapsed}")


        # print (gridgen.grid_shapes)

    print (np.average(counts))




if __name__ == '__main__':
    gen_multi_grids_getstats()

