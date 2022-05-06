## Web App
## Let's try to get this stuff working on the web
# git push heroku web_version:main

from flask import Flask, render_template
import gridgenerate as gridgen
import database_functions as db
from time import time
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




@app.route("/")
@app.route("/index")
def generate_some_grids():
    #now let's try generating a grid
    #global initial variables
    gridgen.num_rows=10
    gridgen.num_cols=10
    gridgen.verbose=False
    gridgen.display_build=False

    # grid = np.zeros((gridgen.num_rows, gridgen.num_cols), dtype=int)
    # grid_shapes = np.zeros((gridgen.num_rows, gridgen.num_cols), dtype=int)

    start_time=time()

    for loop in range(5):
        gridgen.create_blank_grids()
        gridgen.gen_predet_shapes(turtle_fill=False)

    elapsed= time()-start_time

    #now let's work out unique colours for the grid
    shape_colours={}

    shape_coords = gridgen.get_shape_coords()
    for shape_number, shape in shape_coords.items():
        neighbouring_shapes = set()  # empty set
        colours_neighbouring=set()
        for cell in shape:
            neighbours = gridgen.get_neighbours(*cell)
            for nb in neighbours:
                neighbouring_shapes.add(gridgen.grid_shapes[nb])  #will keep unique list
        for n_shape in neighbouring_shapes:
            colours_neighbouring.add(shape_colours.get(n_shape))
        colour_to_try=1
        done=False
        while not done:
            if colour_to_try in colours_neighbouring:
                colour_to_try+=1
            else:
                done=True
        shape_colours[shape_number]=colour_to_try
    print (shape_colours)
    print (max(shape_colours.values()))


    print(gridgen.grid_shapes)


    #now let's try adding grid to database
    doc_name="last_shape"
    to_upsert={"grid_shapes":gridgen.grid_shapes.tolist()}
    #note convert array to list before saving to MongoDB - slight hassle but fair enough
    db.upsert({"name":doc_name},to_upsert)





    '''
    ## function to work out edges
    for r in range(gridgen.num_rows):
        for c in range(gridgen.num_cols):
            this_shape = gridgen.grid_shapes[r,c]
            move_coord = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            edge_thickness=[]
            for move in move_coord:
                if gridgen.grid_shapes(r+move(0),c+move(1))==this_shape:
                    edge_thickness.append("thin")
                else:
                    edge_thickness.append("medium")
    '''


    #return html_out
    return render_template("suguru_grid.html", grid_shapes=gridgen.grid_shapes,elapsed=elapsed, shape_colours=shape_colours)

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




