## Web App
## Let's try to get this stuff working on the web

from flask import Flask
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

    for loop in range(50):
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

    return html_out

@ app.route("/test")
def index():
    print("test called")
    return "test was called"



if __name__ == '__main__':
    app.run()




