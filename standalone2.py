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
    gridgen.num_rows=9 #5
    gridgen.num_cols=7  #7
    gridgen.verbose = False
    gridgen.display_build=False


    # num_success=0
    # num_timeout=0

    gridgen.max_iters = 1e6
    number_to_loop=1 #20

    pick_seed=random.randint(1,10000)
    pick_seed=3589
    print (f"seed {pick_seed}")
    random.seed(pick_seed)

    counts = []
    timing1=[]
    timing2=[]
    timing3=[]
    timing4=[]
    timing5=[]
    results1=0
    results2=0
    results3=0
    results4=0
    results5=0

    common_timeout=3

    for loop in range(number_to_loop):
        start_time = time()

        gridgen.create_blank_grids()
        gridgen.gen_predet_shapes(turtle_fill=False)

        gridgen.shape_coords = gridgen.get_shape_coords()
        print (gridgen.grid_shapes)



        gridgen.iterate_cell_count = 0
        gridgen.iterate_number_count = 0

        gridgen.create_iterate_lookups()
        success, timedout = gridgen.real_iterate(timeout=common_timeout)
        if timedout:
            result = "timedout"
        else:
            result = "success" if success else "fail"
            results1+=1
        elapsed= round(time()-start_time,2)

        legit = gridgen.is_grid_legit()
        print (f"#{loop} ORIG cells iterated {gridgen.iterate_cell_count:,}  result {result}  legit? {legit}  time {elapsed},  ")
        #print(gridgen.grid)

        counts.append(gridgen.iterate_cell_count)
        timing1.append(elapsed)

        # ##NOW TRY A SECOND ATTEMPT TO SOLVE -- a different way
        # #SUPERSEDED -- BETTER SOLVER!
        # start_time = time()
        # gridgen.create_blank_grids(values_only=True)
        # gridgen.iterate_cell_count = 0
        # gridgen.iterate_number_count = 0
        # success, timedout = gridgen.real_iterate_least(timeout=1)
        # elapsed = round(time() - start_time, 2)
        # print(f"Least Solver- #{loop}, cells iterated {gridgen.iterate_cell_count:,} number count {gridgen.iterate_number_count},  success? {success}, timedout? {timedout},   time {elapsed}")
        # print(gridgen.grid)
        # print("Legit? ", gridgen.is_grid_legit())

        ##NOW TRY A THIRD ATTEMPT TO SOLVE -- hopeufully quicker

        start_time = time()
        gridgen.create_blank_grids(values_only=True)
        gridgen.iterate_cell_count = 0
        gridgen.iterate_number_count = 0
        success,iterations = gridgen.new_iterate(timeout=common_timeout)
        elapsed = round(time() - start_time, 2)
        legit = gridgen.is_grid_legit()
        print(f"#{loop} NEW  cells iterated {iterations:,}  success? {success},  legit? {legit}   time {elapsed}")

        #print(gridgen.grid)
        timing2.append(elapsed)
        if success!="timed out": results2+=1


        #v3=with full least search
        start_time = time()
        gridgen.create_blank_grids(values_only=True)
        success,iterations = gridgen.new_iterate(timeout=common_timeout,always_wholegrid_least=True)
        elapsed = round(time() - start_time, 2)
        legit = gridgen.is_grid_legit()
        print(f"#{loop} NEW -WHOLEGRID  cells iterated {iterations:,}  success? {success},  legit? {legit}   time {elapsed}")
        print()
        print(gridgen.grid)
        timing3.append(elapsed)
        if success!="timed out": results3+=1

        #v4=single location checker
        start_time = time()
        gridgen.create_blank_grids(values_only=True)
        success,iterations = gridgen.new_iterate(timeout=common_timeout,always_wholegrid_least=True,single_location_checker=True)
        elapsed = round(time() - start_time, 2)
        legit = gridgen.is_grid_legit()
        print(f"#{loop} NEW -locationchecker-WHOLEGRID  cells iterated {iterations:,}  success? {success},  legit? {legit}   time {elapsed}")
        print()
        print(gridgen.grid)
        timing4.append(elapsed)
        if success!="timed out": results4+=1


        #v5=single location checker/not wholegrid
        start_time = time()
        gridgen.create_blank_grids(values_only=True)
        success,iterations = gridgen.new_iterate(timeout=common_timeout,single_location_checker=True)
        elapsed = round(time() - start_time, 2)
        legit = gridgen.is_grid_legit()
        print(f"#{loop} NEW -locationchecker-NOT  cells iterated {iterations:,}  success? {success},  legit? {legit}   time {elapsed}")
        print()
        print(gridgen.grid)
        timing5.append(elapsed)
        if success!="timed out": results5+=1






        # print (gridgen.grid_shapes)

    print ("original",np.average(timing1),results1)
    print("new method", np.average(timing2),results2)
    print("new method -- wider", np.average(timing3), results3)
    print("new method -- singlelocation", np.average(timing4), results4)
    print("new method -- singlelocation-notwide", np.average(timing5), results5)

def quick_or_slow_test():
    gridgen.initialise_grid(rows=8,cols=10)

    #set max time per go for each speed
    speeds=[3,1,0.3,0.1,0.02]

    #set total time to test
    total_time=6

    seed=random.randint(1,100000)

    for speed in speeds:
        print()
        print(f"***SPEED {speed} seconds")

        random.seed(seed)
        tried=0
        result_count=0
        success_count=0
        start_time=time()
        iterations_used=[]

        while True:

            tried+=1
            gridgen.create_blank_grids()
            gridgen.gen_predet_shapes(turtle_fill=False,single_cell_upper_limit=0)
            gridgen.get_shape_coords()
            result,iterations=gridgen.new_iterate(speed)
            iterations_used.append(iterations)
            #print (f"#{tried}: result?{result}")
            #print (gridgen.grid)
            if result!="timed out":
                result_count+=1
            if result=="success":
                success_count+=1

            if time()>start_time+total_time:
                break

        print (f"SPEED {speed} TOTAL successes {success_count}, results {result_count} out of {tried}, average iterations {np.mean(iterations_used)}" )










if __name__ == '__main__':
    #cProfile.run('gen_multi_grids_getstats()',filename="speedtest.profile")
    gen_multi_grids_getstats()

    #quick_or_slow_test()
    #cProfile.run('quick_or_slow_test()',filename="speedtest.profile")

