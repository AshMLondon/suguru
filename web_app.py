## Web App
## Let's try to get this stuff working on the web

from flask import Flask, render_template
import gridgenerate as gridgen
from time import time
import pprint


## Start Flask Running
## note to work properly the app.run is at the end after the definitions..
app = Flask(__name__)
print ("flask should be running...")



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






    print(gridgen.grid_shapes)



    html_out = pprint.pformat(gridgen.grid_shapes)

    html_out += "<br/>"

    html_out += f"elapsed = {elapsed}"

    html_out += gridgen.array2string(gridgen.grid_shapes)

    html_out += "<br/>"
    html_out += "<br/><pre>"
    grid_as_list = gridgen.grid_shapes.tolist()
    for line in grid_as_list:
        html_out += str(line)+"<br/>"
    html_out += "</pre>"

    print ("elapsed = ",elapsed)

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
    return render_template("suguru_grid.html", grid_shapes=gridgen.grid_shapes,elapsed=elapsed)

@ app.route("/test")
def index():
    print("test called")
    return "test was called"



if __name__ == '__main__':
    app.run()




