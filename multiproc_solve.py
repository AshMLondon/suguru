import time
import gridgenerate as gridgen
import database_functions as db
from time import time
import requests, random
from helper_functions import solve_via_api
import pprint

import concurrent.futures


def gen_and_solve_one():
    timeout=10
    gridgen.create_blank_grids()
    gridgen.gen_predet_shapes(turtle_fill=False)
    returned = solve_via_api(gridgen.grid_shapes,  timeout=timeout)
    return returned


def gen_and_solve_multi_grids():
    #generate and solve multiple grids and see how we do
    #global initial variables
    gridgen.num_rows=6
    gridgen.num_cols=5
    number_to_loop=2


    start_time=time()
    num_success,num_timeout =0,0

    #create a run_stamp to signify which run and be part of unique id put in database
    letters = "ABCDEFGH"
    run_stamp=(''.join(random.choice(letters) for i in range(4) ))

    #reconnect to database with new collection
    db.connect_suguru_db(collection="solved_grids")


    all_results = []

    





    for loop in range(number_to_loop):

        new_result=gen_and_solve_one()
        all_results.append(new_result)


    print (all_results)

    num_success=0
    num_timeout=0
    for result in all_results:
        if result.get("timed_out"):
            num_timeout+=1

        if result.get("success"):
            num_success+=1
            grid_result=result.get("grid_values")
            print(grid_result)
            # now let's try adding grid to database
            # doc_name = run_stamp + "-" + str(loop)  # TODO - improve on  this /unique somehow!
            #
            # to_upsert = {"grid_shapes": gridgen.grid_shapes.tolist(), "grid_values": grid_result,
            #              "size":size}
            # # note convert array to list before saving to MongoDB - slight hassle but fair enough
            # db.upsert({"name": doc_name}, to_upsert)



    elapsed= round(time()-start_time,1)
    print (elapsed)

    num_fails=number_to_loop-num_success-num_timeout
    print (f"Grids tried: {number_to_loop}, Successes: {num_success}, Fails: {num_fails}, Timeout: {num_timeout}, Total time: {elapsed} ")




if __name__ == '__main__':
    gen_and_solve_multi_grids()


