## Web App

from flask import Flask, render_template, request,session, json

from puzzle import Puzzle


## Start Flask Running
## note to work properly the app.run is at the end after the definitions..
app = Flask(__name__)
app.secret_key="needsomethingtowork"
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True


@app.route("/")
def just_a_little_starting_thing():

    puzzle=Puzzle(5,7)
    puzzle.generate_grid_shapes()
    puzzle.generate_iteration_lookups()
    puzzle.color_shapes()
    puzzle.better_solver()
    puzzle.values=puzzle.solution
    return render_template("puzzle_template.html",puzzle=puzzle)





if __name__ == '__main__':
    app.run()
