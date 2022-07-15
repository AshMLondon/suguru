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

##at some point try  httpie -- good for apis



## Start Flask Running
## note to work properly the app.run is at the end after the definitions..
app = Flask(__name__)
app.secret_key="needsomethingtowork"
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

global colours_neighbouring
colours_neighbouring=[]

# colours_list=[]
# for i in range(8):
#     colours_list.append(gridgen.random_colour())

colours_list = gridgen.random_colour_list()

print("cl",colours_list)


#set globals for jinja templates so I can eg use functions within them
app.jinja_env.globals.update(random_colour=gridgen.random_colour,random_colour_list=gridgen.random_colour_list, colours_neighbouring=colours_neighbouring, colours_list=colours_list)
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
        shape_colours[int(shape_number)] = colour_to_try   #use int to override this using np.int32 as the keys - which mucks up saving in a session
    # print (shape_colours)
    # print (max(shape_colours.values()))
    return shape_colours



##NOW INDIVIDUAL PAGES
# - first choose the size of the grid
# - then generate and display a grid - allow you to type in your guesses
# - then show results - are your guesses correct [so far]



@app.route("/")
@app.route("/index")
def Input_Starting_Parameters():
    #First page - place to set the starting parameters, options etc -- initially just size
    rows=session.get("rows",8)  #remember from current session if restarting
    cols=session.get("cols",8)
    #print(rows,cols)
    return render_template("suguru_dialog.html",rows=rows,cols=cols)


@ app.route ("/generate_puzzle")
def find_and_show_one_puzzle():
    #now we generate a new puzzle of  size requested
    cols=int(request.args.get("width"))
    rows=int(request.args.get("height"))
    #print (rows,cols)
    #save size requested in session for next time
    session["rows"]=rows
    session["cols"]=cols

    # rows=10
    # cols=13
    mini_timeout=0.05
    maxi_timeout=6
    start_time=time()
    goes_needed=1
    while True:
        gridgen.initialise_grid(rows, cols)  #create the blank grids and set global size variables for the size requested
        #gridgen.create_blank_grids()
        gridgen.gen_predet_shapes(turtle_fill=False, single_cell_upper_limit=0)  #generate new grid, using the predetermined shapes approach
        gridgen.get_shape_coords()  #calculate coords needed in other functions TODO: this should really happen with the shape generator
        result, iterations = gridgen.new_iterate(mini_timeout, single_location_checker=True, always_wholegrid_least=False)  #can grid be solved?
        if result=="success":
            break
        if time()>start_time+maxi_timeout:
            break

        goes_needed+=1

    #if solveable, now create a puzzle with just a few clues from the solution



    if result=="success":
        # first some annoying prep - #TODO: put this at start of a function?
        gridgen.create_iterate_lookups()
        gridgen.iterate_cell_count,gridgen.iterate_number_count=0,0
        gridgen.max_iters = 1e7
        #then run function that builds up the puzzle
        solution=gridgen.puzzle_buildup()
    else:
        solution=None

    if solution is None:
        return render_template("first_show_grid_get_input.html", result="timed out", goes_needed=goes_needed)
        #return "Timed Out"
        #TODO: try to stop this  happening with an optimised multi solver

    shape_colours = get_unique_colours()
    # print ("shape_colours",shape_colours)


    #save information as session variables before finishing
    session["rows"]=gridgen.num_rows
    session["cols"]=gridgen.num_cols
    session["shape_colours"]=shape_colours
    session["full_grid"]=json.dumps(solution.tolist())
    session["grid_shapes"]=json.dumps(gridgen.grid_shapes.tolist())


    return render_template("first_show_grid_get_input.html", grid_shapes=gridgen.grid_shapes,grid=gridgen.grid,
                           shape_colours=shape_colours, result=result, goes_needed=goes_needed)




@app.route("/check_valid",methods=['GET', 'POST'])
def check_valid():
    # print("GG",gridgen.num_rows)

    grid_shapes = np.array(json.loads(session["grid_shapes"]))
    gridgen.num_rows = session["rows"]
    gridgen.num_cols = session["cols"]

    shape_colours_pre = session["shape_colours"]
    # not sure why but somehow saving in session and loading again makes keys a string - so convert keys to integers
    shape_colours = {int(key): int(value) for key, value in shape_colours_pre.items()}

    #print("loaded shape colours",shape_colours)
    #shape_colours = get_unique_colours()
    #print (grid_shapes)
    rows, cols=grid_shapes.shape
    solution = np.array(json.loads(session["full_grid"]))

    guesses=np.zeros((rows,cols), dtype=int)
    givens=np.zeros((rows,cols), dtype=int)
    missing=0
    error=0
    error_locations=[]
    correct=0
    valid=True

    #print ("FULL GRID",solution)

    for r in range(gridgen.num_rows):
        for c in range(gridgen.num_cols):

            this_guess=request.form.get(f"R{r}C{c}")
            # print(this_guess)
            if this_guess!=None:
                #this cell is in the form  -- so it's not a given (one of numbers given as part of puzzle)
                if this_guess in ["1","2","3","4","5"]:
                    #there is a valid guess here
                    guesses[r,c]=int(this_guess)
                    solution_here=solution[r,c]
                    if int(this_guess) == solution_here:
                        correct+=1
                    else:
                        error+=1
                        error_locations.append((r,c))
                else:
                    #non-valid guess - so basically still a missing number
                    missing+=1
            else:
                #cell was a given - let's rebuild that since we've not saved it
                givens[r,c]=solution[r,c]

    if error:
        result="errors"
        output="There are errors"
    elif missing:
        result="missing"
        output="Correct so far.."
    else:
        result="success"
        output="Success!!"

    output=[output]

    output.append(f"correct={correct}, errors={error}, missing={missing}")

    #TODO:  tidy up result message

    # print (guesses)
    # print (output)

    return render_template("check_guesses.html", grid_shapes=grid_shapes, grid=givens, guesses=guesses, error_locations=error_locations,
                           shape_colours=shape_colours, result="success", text_output=output)






@ app.route("/test")
def index():
    print("test called")
    return "test was called"

@app.route("/setsession")
def setsession():
    test=np.zeros((10,10), dtype=int)
    for r in range(10):
        for c in range(10):
            pass
            # test[r,c]=random.randint(1,5)
    session["test"]=json.dumps(test.tolist())

    return "hmm"


if __name__ == '__main__':
    app.run()






