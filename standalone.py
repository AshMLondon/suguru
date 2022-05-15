import gridgenerate as gridgen
import database_functions as db
import numpy as np
from time import time
import requests, pprint


def findandsolvegrids():
    ######JUST STARTING THIS
    #find multiple grids from database and try solving
    #global initial variables
    gridgen.num_rows=5   #probably not the way we want to keep that going
    gridgen.num_cols=7
    gridgen.verbose=False
    gridgen.display_build=False

    overall_start_time=time()
    num_success=0
    num_timeout=0
    number_to_loop=11 #11 is good for getting up to 10x12
    api_solve=True #False

    gridgen.max_iters = 1e8 #not really - should be overridden
    timeout=None #250 #seconds


    print(f"TIMEOUT DEFAULT: {gridgen.max_iters}")

    for loop in range(number_to_loop):
        per_loop_start_time=time()
        #need to find from database
        doc_name = f"{gridgen.num_rows},{gridgen.num_cols}"  # name is dimensions
        doc_data  = db.my_db_collection.find_one({"name": doc_name})

        #print(f"doc name: {doc_name}")
        print()
        print("from db:",doc_data.get("rows"),doc_data.get("cols"))
        grid_shapes=np.array(doc_data.get("grid_shapes"))
        #print (grid_shapes)


        if api_solve:
            returned=solve_via_api(grid_shapes,max_iters=gridgen.max_iters)
            success = returned.get("success")
            timed_out=returned.get("timed_out")
            grid_result = returned.get("grid_values")


        else:

            gridgen.grid_shapes=grid_shapes
            gridgen.grid = np.zeros((gridgen.num_rows, gridgen.num_cols), dtype=int)
            gridgen.shape_coords = gridgen.get_shape_coords()

            gridgen.iterate_cell_count = 0
            gridgen.iterate_number_count = 0
            gridgen.create_iterate_lookups()

            success,timed_out = gridgen.real_iterate(timeout=timeout)
            grid_result=gridgen.grid


        if timed_out:
            num_timeout+=1
            print ("TIMEOUT")
        else:
            if success:
                num_success+=1
                print ("SUCCESS")
            else:
                print ("FAIL")

        elapsed= round(time()-per_loop_start_time,2)
        print (f"grid size {gridgen.num_rows},{gridgen.num_cols}   elapsed {elapsed}")
        print (grid_result  )

        # #now save to database
        # doc_name = f"{gridgen.num_rows},{gridgen.num_cols}"  #name is dimensions
        # to_upsert = {"record_type":"for_time_trial", "rows":gridgen.num_rows, "cols":gridgen.num_cols,
        #              "generator_type":"standard predef shapes",
        #             "grid_shapes": gridgen.grid_shapes.tolist()}
        # db.upsert({"name": doc_name}, to_upsert)



        if loop%2==0:
            gridgen.num_rows+=1
        else:
            gridgen.num_cols+=1

    overall_elapsed = round(time() - overall_start_time, 2)
    print(f"Total grids {number_to_loop}, Success: {num_success}, Fail: {number_to_loop-num_success-num_timeout}  Timeout {num_timeout}")
    print ("TOTAL TIME OVERALL",overall_elapsed)


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



def genandsavegrids():
    #generate and save  multiple grids
    #global initial variables
    gridgen.num_rows=5
    gridgen.num_cols=7
    gridgen.verbose=False
    gridgen.display_build=False

    start_time=time()
    # num_success=0
    # num_timeout=0
    number_to_loop=11 #11 is good for getting up to 10x12
    for loop in range(number_to_loop):
        gridgen.create_blank_grids()
        gridgen.gen_predet_shapes(turtle_fill=False)

        # gridgen.shape_coords = gridgen.get_shape_coords()
        # gridgen.max_iters = 1e6
        # gridgen.iterate_cell_count = 0
        # gridgen.iterate_number_count = 0
        #
        # gridgen.create_iterate_lookups()
        # success = gridgen.real_iterate()
        # #TODO refactor so success is yes/no/timeout
        # if gridgen.iterate_cell_count>=gridgen.max_iters:
        #     num_timeout+=1
        # else:
        #     if success:
        #         num_success+=1

        elapsed= round(time()-start_time,2)
        print (f"grid size {gridgen.num_rows},{gridgen.num_cols}   elapsed {elapsed}")
        print (gridgen.grid_shapes)

        #now save to database
        doc_name = f"{gridgen.num_rows},{gridgen.num_cols}"  #name is dimensions
        to_upsert = {"record_type":"for_time_trial", "rows":gridgen.num_rows, "cols":gridgen.num_cols,
                     "generator_type":"standard predef shapes",
                    "grid_shapes": gridgen.grid_shapes.tolist()}
        db.upsert({"name": doc_name}, to_upsert)



        if loop%2==0:
            gridgen.num_rows+=1
        else:
            gridgen.num_cols+=1




if __name__ == '__main__':
    db.connect_suguru_db()
    #genandsavegrids()  #'do just once usually
    findandsolvegrids()
