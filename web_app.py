## Web App
## Let's try to get this stuff working on the web
# git push heroku new_web_multiple:main

import gridgenerate as gridgen
from helper_functions import solve_via_api

from flask import Flask, render_template, request

import database_functions as db
from time import time
import requests, random
import pprint



## Start Flask Running
## note to work properly the app.run is at the end after the definitions..
app = Flask(__name__)
global colours_neighbouring
colours_neighbouring=[]

#set globals for jinja templates so I can eg use functions within them
app.jinja_env.globals.update(random_colour=gridgen.random_colour, colours_neighbouring=colours_neighbouring)
print ("flask should be running...")

##Initialise DB
result = db.connect_suguru_db()

## END OF SETUP -- NOW INDIVIDUAL PAGES

def get_unique_colours():
    # TODO - ship this out as a function
    # now let's work out unique colours for the grid
    shape_colours = {}
    shape_coords = gridgen.get_shape_coords()
    for shape_number, shape in shape_coords.items():
        neighbouring_shapes = set()  # empty set
        colours_neighbouring = set()
        for cell in shape:
            neighbours = gridgen.get_neighbours(*cell)
            for nb in neighbours:
                neighbouring_shapes.add(gridgen.grid_shapes[nb])  # will keep unique list
        for n_shape in neighbouring_shapes:
            colours_neighbouring.add(shape_colours.get(n_shape))
        colour_to_try = 1
        done = False
        while not done:
            if colour_to_try in colours_neighbouring:
                colour_to_try += 1
            else:
                done = True
        shape_colours[shape_number] = colour_to_try
    # print (shape_colours)
    # print (max(shape_colours.values()))
    return shape_colours


@app.route("/")
@app.route("/index")
def generate_some_grids():
    #now let's try generating a grid
    #global initial variables
    gridgen.num_rows=8
    gridgen.num_cols=9
    gridgen.verbose=False
    gridgen.display_build=False

    # grid = np.zeros((gridgen.num_rows, gridgen.num_cols), dtype=int)
    # grid_shapes = np.zeros((gridgen.num_rows, gridgen.num_cols), dtype=int)

    start_time=time()
    for loop in range(1):
        gridgen.create_blank_grids()
        gridgen.gen_predet_shapes(turtle_fill=False)
    elapsed= time()-start_time

    shape_colours = get_unique_colours()
    print(gridgen.grid_shapes)


    #now let's try adding grid to database
    doc_name="last_generating_shape"
    to_upsert={"grid_shapes":gridgen.grid_shapes.tolist()}
    #note convert array to list before saving to MongoDB - slight hassle but fair enough
    db.upsert({"name":doc_name},to_upsert)

    #return html_out
    return render_template("suguru_grid.html", grid_shapes=gridgen.grid_shapes,elapsed=elapsed, shape_colours=shape_colours)


@app.route("/solve")
def gen_and_solve_multi_grids():
    #generate and solve multiple grids and see how we do
    #global initial variables
    gridgen.verbose=False
    gridgen.display_build=False


    #now some defaults that will get overwritten if
    gridgen.num_rows=6
    gridgen.num_cols=5
    number_to_loop=5
    timeout=4
    max_iters = None  # no default as timeout is default
    api_solve = True
    shuffle_slightly=True

    #now overwrite
    args=request.args
    size=args.get("size")
    if size:
        if "x" in size:
            size_split=size.split("x")
            print (size_split)
            gridgen.num_rows,gridgen.num_cols=int(size_split[0]),int(size_split[1])
    else:
        size=str(gridgen.num_rows)+"x"+str(gridgen.num_cols)  #for database entry

    timeout=int(args.get("timeout",timeout))
    if args.get("max_iters"):
        max_iters = float(args.get("max_iters"))
        timeout=None
    number_to_loop=int(args.get("number",number_to_loop))
    api_solve=not args.get("api",api_solve)=="False"  #just converting string doesnt seem to work
    url_override = None
    if args.get("api")=="local":
        url_override="http://127.0.0.5:5000/solve_grid_api"
    elif timeout>28:
        timeout=28  #max out timeout at 28 secs if heroku

    if args.get("shuffle")=="False":
        shuffle_slightly=False


    print(gridgen.num_rows,"x",gridgen.num_cols,number_to_loop,"loops",timeout,"s")
    start_time=time()
    num_success,num_timeout =0,0
    #create a run_stamp to signify which run and be part of unique id put in database
    letters = "ABCDEFGH"
    run_stamp=(''.join(random.choice(letters) for i in range(4) ))




    #reconnect to database with new collection
    db.connect_suguru_db(collection="solved_grids")



    for loop in range(number_to_loop):
        gridgen.create_blank_grids()
        gridgen.gen_predet_shapes(turtle_fill=False,shuffle_slightly=shuffle_slightly)

        #that's generated -- now solve


        if api_solve:
            returned=solve_via_api(gridgen.grid_shapes,max_iters=max_iters, timeout=timeout,url_override=url_override)
            success = returned.get("success")
            timed_out=returned.get("timed_out")
            grid_result = returned.get("grid_values")


        else:

            gridgen.shape_coords = gridgen.get_shape_coords()

            gridgen.max_iters = max_iters
            gridgen.iterate_cell_count = 0
            gridgen.iterate_number_count = 0

            gridgen.create_iterate_lookups()
            success, timed_out  = gridgen.real_iterate(timeout=timeout)
            grid_result=gridgen.grid


        if timed_out:
            num_timeout+=1

        if success:
            num_success+=1
            print(grid_result)
            # now let's try adding grid to database
            doc_name = run_stamp + "-" + str(loop)  # TODO - improve on  this /unique somehow!

            to_upsert = {"grid_shapes": gridgen.grid_shapes.tolist(), "grid_values": grid_result,
                         "size":size}
            # note convert array to list before saving to MongoDB - slight hassle but fair enough
            db.upsert({"name": doc_name}, to_upsert)





    elapsed= round(time()-start_time,1)
    print (elapsed)

    #shape_colours = get_unique_colours()
    #print(gridgen.grid_shapes)
    num_fails=number_to_loop-num_success-num_timeout
    html_out=f"Grids tried: {number_to_loop}, Successes: {num_success}, Fails: {num_fails}, Timeout: {num_timeout}, Total time: {elapsed} "
    html_out+=f" max_iters: {max_iters} Api:{api_solve}"
    return html_out




    #return html_out
    #   return render_template("suguru_grid.html", grid=gridgen.grid, grid_shapes=gridgen.grid_shapes, elapsed=elapsed, shape_colours=shape_colours)




@app.route("/singlesolve")
def gen_and_solve_one_grids():
    #now let's try generating a grid an solving it too
    #global initial variables
    gridgen.num_rows=8
    gridgen.num_cols=9
    gridgen.verbose=False
    gridgen.display_build=False

    # grid = np.zeros((gridgen.num_rows, gridgen.num_cols), dtype=int)
    # grid_shapes = np.zeros((gridgen.num_rows, gridgen.num_cols), dtype=int)

    start_time=time()
    for loop in range(1):
        gridgen.create_blank_grids()
        gridgen.gen_predet_shapes(turtle_fill=False)

        gridgen.shape_coords = gridgen.get_shape_coords()

        gridgen.max_iters = 1e6
        gridgen.iterate_cell_count = 0
        gridgen.iterate_number_count = 0

        gridgen.create_iterate_lookups()
        success, timed_out = gridgen.real_iterate()



    elapsed= time()-start_time

    shape_colours = get_unique_colours()
    print(gridgen.grid_shapes)


    #now let's try adding grid to database
    doc_name="last_solving_shape"
    to_upsert={"grid_shapes":gridgen.grid_shapes.tolist(),"grid_values":gridgen.grid.tolist()}
    #note convert array to list before saving to MongoDB - slight hassle but fair enough
    db.upsert({"name":doc_name},to_upsert)

    #return html_out
    return render_template("suguru_grid.html", grid=gridgen.grid, grid_shapes=gridgen.grid_shapes, elapsed=elapsed, shape_colours=shape_colours)


def ZZsolve_via_api(grid_to_try, max_iters=None, timeout=None):
    '''
    function to call the api on heroku to get a faster response using pypy
    :param grid_shapes:
    :return:
    '''
    params={"grid_shapes":grid_to_try.tolist()}  #convert np.array to list
    if max_iters:
        params["max_iters"]=max_iters
    if timeout:
        params["timeout"]=timeout

    #url_send="http://127.0.0.1:5000/solve_grid_api"
    url_send="https://sugurupypy.herokuapp.com/solve_grid_api"
    response = requests.post(url_send, json=params)
    json_back=response.json()
    #pprint.pprint (json_back)
    #print (json_back.get("grid_values"))
    return json_back





@ app.route("/test")
def index():
    print("test called")
    return "test was called"



@ app.route("/config")
def config_test():
    EV=os.environ.get("SUGURU_USER")
    if not EV: EV="didn't find"
    print(EV)
    print(os.environ.get("OneDrive"))
    print(os.environ.get("BLAH"))
    return EV

@ app.route("/dbtest")
def db_test():


    my_db_collection = db.my_db_collection
    doc_count = my_db_collection.count_documents({})
    print(doc_count)

    result=db.upsert({"name":"test"},{"entry":"hello!"})
    print (result)


    return(str(doc_count))




if __name__ == '__main__':
    app.run()




