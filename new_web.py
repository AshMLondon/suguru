## Web App
## Let's try to get this stuff working on the web
# git push heroku new_web_multiple:main
import numpy as np

import gridgenerate as gridgen
#from helper_functions import solve_via_api

from flask import Flask, render_template, request,session, json

#import database_functions as db
from time import time
import requests, random
import pprint



## Start Flask Running
## note to work properly the app.run is at the end after the definitions..
app = Flask(__name__)
app.secret_key="needsomethingtowork"
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

global colours_neighbouring
colours_neighbouring=[]

#set globals for jinja templates so I can eg use functions within them
app.jinja_env.globals.update(random_colour=gridgen.random_colour, colours_neighbouring=colours_neighbouring)
print ("flask should be running...")


## END OF SETUP -- NOW INDIVIDUAL PAGES

def get_unique_colours():
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
def input_params():
    rows=session.get("rows",8)
    cols=session.get("cols",8)
    print(rows,cols)
    return render_template("suguru_dialog.html",rows=rows,cols=cols)


@ app.route ("/generate_puzzle")
def find_and_show_one_puzzle():
    cols=int(request.args.get("width"))
    rows=int(request.args.get("height"))
    print (rows,cols)

    #save in session for next time
    session["rows"]=rows
    session["cols"]=cols

    # rows=10
    # cols=13
    mini_timeout=0.05
    maxi_timeout=6
    start_time=time()
    while True:
        gridgen.initialise_grid(rows, cols)
        gridgen.create_blank_grids()
        gridgen.gen_predet_shapes(turtle_fill=False, single_cell_upper_limit=0)
        gridgen.get_shape_coords()
        result, iterations = gridgen.new_iterate(mini_timeout, single_location_checker=True, always_wholegrid_least=False)
        if result=="success":
            break
        if time()>start_time+maxi_timeout:
            break

    gridgen.create_iterate_lookups()
    gridgen.iterate_cell_count,gridgen.iterate_number_count=0,0
    gridgen.max_iters = 1e6

    gridgen.puzzle_buildup()

    shape_colours = get_unique_colours()

    session["full_grid"]=json.dumps(gridgen.grid.tolist())

    return render_template("suguru_new_grid_input.html", grid_shapes=gridgen.grid_shapes,grid=gridgen.grid,
                           shape_colours=shape_colours, result=result)


@app.route("/check_valid")
def check_valid():
    # print("GG",gridgen.num_rows)
    guesses=np.zeros((gridgen.num_rows,gridgen.num_cols), dtype=int)
    missing=0
    valid=True

    solution=np.array(json.loads(session["full_grid"]))
    print ("FULL GRID",solution)

    for r in range(gridgen.num_rows):
        for c in range(gridgen.num_cols):
            ##TODO: need to find a way to know what the givens are -- either through including in the form or using a session variable
            this_guess=request.args.get(f"R{r}C{c}")
            print(this_guess)
            if this_guess in ["1","2","3","4","5"]:
                guesses[r,c]=int(this_guess)


    print (guesses)
    return str(guesses.tolist())



@ app.route("/test")
def index():
    print("test called")
    return "test was called"



if __name__ == '__main__':
    app.run()





