## Web No Numpy Solver
## solver version with No Numpy used - idea is to then use PyPy to run so it's fast (PyPy doesn't seem to cope with Numpy)
# git push heroku_pypy  standalone:main

#for special heroku setup:
#needs its own runtime.txt to specify pypy -- version I managed to get working was:  pypy3.6-7.3.2
#needs its own requirements.txt  --- seems like this needs editing to be lower versions in many cases

# remember to update heroku environment variables to allow database to connect!



from flask import Flask, render_template, jsonify, request
import requests
import database_functions as db
import time, platform, pprint
from time import time


##INITIALISATION


## Start Flask Running
## note to work properly the app.run is at the end after the definitions..
app = Flask(__name__)

##Initialise DB
result = db.connect_suguru_db()

## END OF SETUP -- NOW INDIVIDUAL PAGES




def get_shape_coords(grid_shapes):
    global shape_coords, r, c, this_shape, num_rows, num_cols
    shape_coords = {}
    for r in range(num_rows):
        for c in range(num_cols):
            this_shape = grid_shapes[r][c]
            this_shape_coords = shape_coords.get(this_shape)
            if not this_shape_coords:
                this_shape_coords = []
            this_shape_coords.append((r, c))
            shape_coords[this_shape] = this_shape_coords

    return shape_coords

def create_iterate_lookups(grid_shapes):
    global iter_shapes, iter_nonshape_neighbours, row_col
    # to save time with a large recursive function, use some additional data lookups
    iter_shapes = {}  # not working yet!!
    iter_nonshape_neighbours = {}
    row_col = {}
    for i in range(num_cols * num_rows):
        r = i // num_cols
        c = i % num_cols
        row_col[i] = (r, c)
        shape_no = grid_shapes[r][c]
        shapes = shape_coords[shape_no]
        max_nums = len(shapes)
        iter_shapes[i] = (max_nums, shapes)
        neighbours = get_neighbours(r, c)
        for nb in neighbours:
            if nb in shapes:
                neighbours.remove(nb)
        iter_nonshape_neighbours[i] = neighbours

def get_neighbours(r, c):
    neighbours = []
    for nb_r in range(r - 1, r + 2):
        if 0 <= nb_r <= num_rows - 1:
            for nb_c in range(c - 1, c + 2):
                if 0 <= nb_c <= num_cols - 1:
                    neighbours.append((nb_r, nb_c))
    neighbours.remove((r, c))  # don't include itself
    return neighbours



def non_np_real_iterate(grid_shapes,timeout=None):
    '''
    main iteration function
    :param grid_shapes:
    :param timeout:
    :return:
    '''
    # really iterate , not just recursive
    global iterate_number_count, iterate_cell_count, max_iters, verbose,iterate_number_count, start_time, num_rows,num_cols
    if timeout:
        timeout_time=time()+timeout
    success = False

    #create blank grid
    grid=[]
    for r in range(num_rows):
        grid.append(list(0 for i in range(0, num_cols)))
    print(grid)

    numbers_to_try_stack = {}
    cell_iter_no = 0
    keep_iterating = True
    timed_out = False
    next_step = "starting"
    while keep_iterating:
        # let's start loop off
        # print("next step",next_step)
        if next_step == "ascend":
            if cell_iter_no < num_rows * num_cols - 1:  # TODO create variable
                cell_iter_no += 1
                iterate_cell_count += 1

            else:
                # got as far as end cell - complete
                print("*complete*")
                success = True
                break

        if next_step == "descend":
            grid[rc[0]][rc[1]] = 0
            cell_iter_no -= 1
            if cell_iter_no < 0:
                next_step = "FAIL"
                break

        rc = row_col[cell_iter_no]
        #print ("rc",rc)

        if next_step == "ascend" or next_step == "starting":
            max_nums, shapes = iter_shapes[cell_iter_no]
            nums_avail = list(range(1, max_nums + 1))
            for shape in shapes:
                this_num = grid[shape[0]][shape[1]]
                #print (this_num,nums_avail)
                if this_num in nums_avail:
                    nums_avail.remove(this_num)
            numbers_to_try_stack[cell_iter_no] = nums_avail

        elif next_step == "descend":
            max_nums, shapes = iter_shapes[cell_iter_no]  # TODO do we need shapes now?
            nums_avail = numbers_to_try_stack[cell_iter_no]

        # now we actually iterate do we?
        # print ("where we're at",cell_iter_no,nums_avail)

        if not nums_avail:
            # run out of numbers for cell, retreat
            next_step = "descend"
        else:
            num_to_try = nums_avail.pop(0)
            numbers_to_try_stack[cell_iter_no] = nums_avail

            grid[rc[0]][rc[1]] = num_to_try
            #print (f"set {num_to_try} at {r},{c}")
            iterate_number_count += 1
            # now let's check if valid
            valid = True
            neighbours = iter_nonshape_neighbours[cell_iter_no]
            for nb in neighbours:
                if grid[nb[0]][nb[1]] == num_to_try:
                    valid = False
                    break

            # if ok - ascend a level in iteration
            if valid:
                if timeout:
                    ok_continue=(time()<timeout_time)
                else:
                    ok_continue=(iterate_cell_count<max_iters)
                if cell_iter_no < num_rows * num_cols - 1 and ok_continue:
                    iterate_cell_count += 1
                    next_step = "ascend"
                    if iterate_cell_count % 10 == 0:
                        elapsed = time() - start_time
                        if not elapsed:
                            rate = 0
                        else:
                            rate = iterate_cell_count / elapsed
                        print("iterate counts", iterate_cell_count, iterate_number_count, "time", elapsed,
                              "rate", rate)

                else:
                    if not ok_continue:
                        #if we timed out, set flag
                        timed_out=True


            else:
                # doesn't work try next number
                next_step = "inc_number"
                grid[rc[0]][rc[1]] = 0

        # this is end of while loop I think

    # print(grid)
    # END OF ITERATION
    return grid,success,timed_out






@ app.route("/")
def simple_test():
    return "simple test!"

@ app.route("/solve")
def nonp_findandsolvegrids_fromDB():
    ######JUST STARTING THIS
    #find multiple grids from database and try solving
    #global initial variables
    global num_rows,num_cols, iterate_number_count, iterate_cell_count, max_iters
    num_rows=5   #probably not the way we want to keep that going
    num_cols=7
    verbose=False
    display_build=False

    overall_start_time=time()
    num_success=0
    num_timeout=0
    number_to_loop=2 #11 is good for getting up to 10x12

    max_iters = 3e6
    timeout=None #250 #seconds


    print(f"TIMEOUT DEFAULT: {max_iters}")

    for loop in range(number_to_loop):
        per_loop_start_time=time()
        #need to find from database
        doc_name = f"{num_rows},{num_cols}"  # name is dimensions
        doc_data  = db.my_db_collection.find_one({"name": doc_name})

        #print(f"doc name: {doc_name}")
        print()
        print("from db:",doc_data.get("rows"),doc_data.get("cols"))
        grid_shapes=doc_data.get("grid_shapes")
        print (grid_shapes)





        shape_coords = get_shape_coords(grid_shapes)
        #print(shape_coords)

        iterate_cell_count = 0
        iterate_number_count = 0
        create_iterate_lookups(grid_shapes)
        # print(iter_shapes)
        # print(iter_nonshape_neighbours)
        # print(row_col)
        # print()


        grid,success,timed_out = non_np_real_iterate(grid_shapes,timeout=timeout)
        #TODO refactor so success is yes/no/timeout

        if iterate_cell_count>=max_iters:
            num_timeout+=1
            print ("TIMEOUT")
        else:
            if success:
                num_success+=1
                print ("SUCCESS")

        elapsed= round(time()-per_loop_start_time,2)
        print (f"grid size {num_rows},{num_cols}   elapsed {elapsed}")
        print (grid)

        # #now save to database
        # doc_name = f"{gridgen.num_rows},{gridgen.num_cols}"  #name is dimensions
        # to_upsert = {"record_type":"for_time_trial", "rows":gridgen.num_rows, "cols":gridgen.num_cols,
        #              "generator_type":"standard predef shapes",
        #             "grid_shapes": gridgen.grid_shapes.tolist()}
        # db.upsert({"name": doc_name}, to_upsert)



        if loop%2==0:
            num_rows+=1
        else:
            num_cols+=1
            


    overall_elapsed = round(time() - overall_start_time, 2)
    print()
    print (f"TOTAL TIME OVERALL  {overall_elapsed}")

    html_out=f"Grids {number_to_loop}, Timeout {timeout}, Maxiters {max_iters}  <br/>"

    html_out += f"TOTAL TIME OVERALL  {overall_elapsed} <br/>"

    html_out += f"Python impl: {platform.python_implementation()} <br/>"

    to_return={"grid_vales":grid,"success":success,"loadofstringstuff":html_out,"original_grid_shapes_in":grid_shapes}

    return jsonify(to_return)

@ app.route("/solve_grid_api",methods=["GET"])
def api_info():
    return('''Api. Need to POST JSON with grid_shapes =nested list of shapes.<br/>
           Optional timeout: either timeout= seconds, max_iters = number of iterations. If neither defaults
           <br/>returns JSON including solution grid_values and whether solved''')

@ app.route("/solve_grid_api",methods=["POST"])
def solve_grid_api():
    #take a set of grid shapes in and then solve it
    global num_rows, num_cols, iterate_number_count, iterate_cell_count, max_iters
    if request.is_json:
        submitted=request.get_json()
        grid_shapes=submitted.get("grid_shapes")
        print("target...",grid_shapes)
        if grid_shapes:
            num_rows=len(grid_shapes)
            num_cols=len(grid_shapes[0])
            print("target...", num_rows,num_cols)

            #now solve the grid

            #TODO - Refactor so all this preliminary stuff done in one place
            start_time=time()
            shape_coords = get_shape_coords(grid_shapes)
            iterate_cell_count = 0
            iterate_number_count = 0

            timeout=submitted.get("timeout")
            max_iters=submitted.get("max_iters")

            if not (timeout or max_iters):
                timeout=10   #at least set a default


          #second figure is default
            create_iterate_lookups(grid_shapes)
            grid, success,timed_out = non_np_real_iterate(grid_shapes, timeout=timeout)

            result_to_send={"success": success, "time_elapsed":time()-start_time,
                            "grid_values":grid, "timed_out":timed_out,"rows":num_rows,"cols":num_cols,
                            "iterations_used":iterate_cell_count,"timeout":timeout,"max_iters":max_iters,"grid_shapes":grid_shapes}
            return jsonify(result_to_send),201

        else:
            return {"error": "Request must be JSON"}, 415










@ app.route("/api_target_test",methods=["POST"])
def api_target_test():
    #this is JUST A TEST to test out the POST  passing of data as input to what's going to be my API
    if request.is_json:
        submitted=request.get_json()
        grid_shapes=submitted.get("grid_shapes")
        print("target...",grid_shapes)
        if grid_shapes:
            num_rows=len(grid_shapes)
            num_cols=len(grid_shapes[0])
            print("target...", num_rows,num_cols)

            result_to_send={"result": "grid shapes sent", "rows":num_rows,"cols":num_cols,"grid_shapes":grid_shapes}
            return jsonify(result_to_send),201

        else:
            return {"error": "Request must be JSON"}, 415


@ app.route("/sendtest")
def sendtest():
    #this is testing out the API on the LOCAL machine

    grid_to_try=    [[3,3,3,2,4,4,5],[3,1,2,2,2,4,5],
                     [1,1,1,2,6,4,5],[10,1,8,6,6,4,5],[8,8,8,6,7,7,5],[9,9,8,6,7,7,7]]
    #this 6x7 grid starting 3,3,3 is known to be solvable

    params={"grid_shapes":grid_to_try}
    url_send="http://127.0.0.1:5000/solve_grid_api"  # "https://sugurupypy.herokuapp.com/solve"

    response = requests.post(url_send, json=params)

    print (response)
    json_back=response.json()
    pprint.pprint (json_back)
    print (json_back.get("grid_values"))

    #html_string=f"Grid solver API. Success {json_back.get("success")}"

    #return "have called - look at print "
    return json_back






if __name__ == '__main__':
    app.run()