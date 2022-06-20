import gridgenerate as gridgen
import database_functions as db
import numpy as np
from time import time
import requests, pprint, random, cProfile


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
    gridgen.num_rows=8 #5
    gridgen.num_cols=10  #7
    gridgen.verbose = False
    gridgen.display_build=False


    # num_success=0
    # num_timeout=0
    counts=[]
    gridgen.max_iters = 1e6
    number_to_loop=1

    pick_seed=random.randint(1,10000)
    #pick_seed=8211
    print (f"seed {pick_seed}")
    random.seed(pick_seed)


    for loop in range(number_to_loop):
        start_time = time()

        gridgen.create_blank_grids()
        gridgen.gen_predet_shapes(turtle_fill=False)

        gridgen.shape_coords = gridgen.get_shape_coords()
        print (gridgen.grid_shapes)



        gridgen.iterate_cell_count = 0
        gridgen.iterate_number_count = 0

        gridgen.create_iterate_lookups()
        success, timedout = gridgen.real_iterate()
        elapsed= round(time()-start_time,2)

        print (f"#{loop}, cells iterated {gridgen.iterate_cell_count:,}  success? {success}, timedout? {timedout},   time {elapsed}")
        print(gridgen.grid)
        print("Legit? ",gridgen.is_grid_legit())
        counts.append(gridgen.iterate_cell_count)

        ##NOW TRY A SECOND ATTEMPT TO SOLVE -- a different way
        #SUPERSEDED -- BETTER SOLVER!
        start_time = time()
        gridgen.create_blank_grids(values_only=True)
        gridgen.iterate_cell_count = 0
        gridgen.iterate_number_count = 0
        success, timedout = gridgen.real_iterate_least(timeout=1)
        elapsed = round(time() - start_time, 2)
        print(f"Least Solver- #{loop}, cells iterated {gridgen.iterate_cell_count:,} number count {gridgen.iterate_number_count},  success? {success}, timedout? {timedout},   time {elapsed}")
        print(gridgen.grid)
        print("Legit? ", gridgen.is_grid_legit())

        ##NOW TRY A THIRD ATTEMPT TO SOLVE -- hopeufully quicker

        start_time = time()
        gridgen.create_blank_grids(values_only=True)
        gridgen.iterate_cell_count = 0
        gridgen.iterate_number_count = 0
        success,iterations = gridgen.new_iterate()
        elapsed = round(time() - start_time, 2)
        print(f"Least Solver- #{loop}, cells iterated {iterations:,}  success? {success},   time {elapsed}")
        print(gridgen.grid)
        print("Legit? ", gridgen.is_grid_legit())



        # print (gridgen.grid_shapes)

    print (np.average(counts))




if __name__ == '__main__':
    cProfile.run('gen_multi_grids_getstats()',filename="speedtest.profile")
    #gen_multi_grids_getstats()

