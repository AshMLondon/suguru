## Web App

import random
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

    puzzle=Puzzle(7,8)
    # random.seed(2)
    puzzle.generate_grid_shapes()
    puzzle.generate_iteration_lookups()
    puzzle.smaller_surrounded_check_all()  #***
    puzzle.colour_shapes()
    success= puzzle.better_solver(multi=False)  #look for single solution to begin
    print("Success?",success, "iterations",puzzle.iteration_counter, "Timeout?",puzzle.iteration_timeout)

    if success:
        puzzle.build_up_givens()
    puzzle.values=puzzle.solution

    # return render_template("puzzle_template.html", puzzle=puzzle)


    #save completed puzzle in session that can be reloaded next time we come back for a page
    session["size"]=(puzzle.rows,puzzle.cols)
    session["shapes"]=puzzle.shapes
    session["solution"]=puzzle.solution
    session["givens"]=puzzle.givens
    session["colour_allocation"]= puzzle.shape_colours


    return render_template("puzzle_template.html",puzzle=puzzle)

@app.route("/load")
def run_thru_saved():


    puzzle=Puzzle(7,8)
    with open("grids_7x8","r" ) as file:
        all_puzzles_dict=json.load(file)


    puzzle_counter= int(request.args.get("n",0))



    puzzles_dict=all_puzzles_dict[puzzle_counter]
    print(puzzles_dict)

    puzzle.shapes=puzzles_dict["shapes"]
    puzzle.solutions=puzzles_dict["solution"]
    puzzle.givens=puzzles_dict["givens"]

    puzzle.generate_iteration_lookups()
    puzzle.colour_shapes()

    #save completed puzzle in session that can be reloaded next time we come back for a page
    session["size"]=(puzzle.rows,puzzle.cols)
    session["shapes"]=puzzle.shapes
    session["solution"]=puzzle.solution
    session["givens"]=puzzle.givens
    session["colour_allocation"]= puzzle.shape_colours


    return render_template("puzzle_template.html",puzzle=puzzle,puzzle_counter=puzzle_counter)




@app.route("/check_valid",methods=['GET', 'POST'])
def check_valid():

    #first re-load the puzzle
    #TODO - add error message if you get here without saved session

    rows,cols=session["size"]
    puzzle=Puzzle(rows,cols)
    puzzle.shapes=session["shapes"]
    puzzle.solution=session["solution"]
    puzzle.givens=session["givens"]
    puzzle.shape_colours=session["colour_allocation"]
    #saving in session and loading again makes keys a string - so convert keys to integers
    puzzle.shape_colours = {int(key): int(value) for key, value in puzzle.shape_colours.items()}

    print("loaded shape colours",puzzle.shape_colours)
    #shape_colours = get_unique_colours()
    #print (grid_shapes)


    guesses=[[0 for c in range (cols)] for r in range(rows)]
    givens=[[0 for c in range (cols)] for r in range(rows)]
    missing=0
    error=0
    error_locations=[]
    correct=0
    valid=True

    #print ("FULL GRID",solution)

    for r in range(rows):
        for c in range(cols):

            this_guess=request.form.get(f"R{r}C{c}")
            # print(this_guess)
            if this_guess!=None:
                #this cell is in the form  -- so it's not a given (one of numbers given as part of puzzle)
                if this_guess in ["1","2","3","4","5"]:
                    #there is a valid guess here
                    guesses[r][c]=int(this_guess)
                    solution_here=puzzle.solution[r][c]
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
                givens[r][c]=puzzle.solution[r][c]

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

    return render_template("puzzle_template.html", puzzle=puzzle, message=output, guesses=guesses)






if __name__ == '__main__':
    app.run()
