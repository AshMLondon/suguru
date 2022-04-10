# Suguru test
""""
Suguru Puzzle Solver

by Ashley,  April 2022
"""


def get_neighbours(r, c):
    neighbours = []
    for nb_r in range(r - 1, r + 2):
        if 0 <= nb_r <= num_rows - 1:
            for nb_c in range(c - 1, c + 2):
                if 0 <= nb_c <= num_cols - 1:
                    neighbours.append((nb_r, nb_c))
    neighbours.remove((r, c))  # don't include itself
    return neighbours


def display_newnumber(num, rc_tuple, colour="blue"):
    xpos = start_coords[0] + cell_draw_size * rc_tuple[1] + horiz_offset
    ypos = start_coords[1] - cell_draw_size * rc_tuple[0] - vert_offset  # down is negative
    pen.setpos(xpos, ypos)
    pen.color(colour)
    pen.write(num, align="center", font=("Comic Sans MS", 18, "normal"))
    #print("number =", grid[r, c])
    # time.sleep(0.05)


import turtle, time
import numpy as np

# SETUP
num_cols = 13
num_rows = 10
cell_draw_size = 40

# grid=np.zeros((num_rows, num_cols), dtype=int)
# grid_shapes=np.zeros((num_rows, num_cols), dtype=int)


numbers_given_CSV = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0],
    [0, 0, 0, 5, 3, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 2, 0],
    [0, 0, 0, 0, 0, 0, 0, 5, 3, 0, 4, 0, 0],
    [0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0],
    [0, 0, 1, 0, 0, 0, 3, 0, 2, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

shape_as_CSV = [
    [1, 1, 1, 2, 3, 3, 3, 4, 4, 4, 5, 6, 6],
    [7, 8, 2, 2, 2, 9, 3, 3, 10, 5, 5, 5, 6],
    [7, 8, 8, 2, 9, 9, 9, 10, 10, 10, 5, 11, 6],
    [7, 7, 8, 12, 12, 9, 13, 13, 10, 14, 11, 11, 6],
    [15, 7, 16, 16, 12, 12, 12, 13, 14, 14, 11, 11, 17],
    [15, 15, 16, 16, 16, 18, 19, 13, 13, 14, 14, 17, 17],
    [15, 20, 20, 20, 18, 18, 18, 21, 22, 22, 23, 17, 24],
    [25, 25, 20, 26, 26, 18, 21, 21, 21, 23, 23, 23, 24],
    [25, 25, 20, 27, 26, 26, 26, 21, 28, 28, 23, 24, 24],
    [27, 27, 27, 27, 29, 29, 29, 29, 28, 28, 28, 24, 30],
]
# use given numbers to create key arrays
grid = np.array(numbers_given_CSV)
grid_shapes = np.array(shape_as_CSV)

# now create a dict of all shapes and their coords
shape_coords = {}
for r in range(num_rows):
    for c in range(num_cols):
        this_shape = grid_shapes[r, c]
        this_shape_coords = shape_coords.get(this_shape)
        if not this_shape_coords:
            this_shape_coords = []
        this_shape_coords.append((r, c))
        shape_coords[this_shape] = this_shape_coords

#print(shape_coords)

# grid[1,11]=5  #*****FORCE TO CHECK


screen = turtle.Screen()
# screen.screensize(0.9,0.8)
# screen.bgcolor("orange")
screen.delay(0)
screen.tracer(0)

pen = turtle.Turtle()
pen.speed(0)
# pen.hideturtle()

start_coords = (-screen.window_width() / 2 + cell_draw_size, screen.window_height() / 2 - cell_draw_size)

row_width = cell_draw_size * (num_cols - 1)
line_light = 1
line_heavy = 3

pen.up()
# pen.setpos(-row_width, +row_width)
pen.setpos(start_coords)
pen.down()
#print(grid.shape)

# DRAW ROWS
for r in range(num_rows + 1):
    for c in range(num_cols):
        pen.width(line_light)
        if r == 0:
            pen.width(line_heavy)
        elif r == num_rows:
            pen.width(line_heavy)
        else:
            if grid_shapes[r - 1, c] != grid_shapes[r, c]: pen.width(line_heavy)
        pen.forward(cell_draw_size)
    pen.right(90)
    pen.up()
    pen.forward(cell_draw_size)
    pen.left(90)
    pen.backward(row_width + cell_draw_size)
    pen.down()

# now columns
pen.up()
pen.setpos(start_coords)
pen.down()
pen.right(90)
for c in range(num_cols + 1):
    for r in range(num_rows):
        pen.width(line_light)
        if c == 0:
            pen.width(line_heavy)
        elif c == num_cols:
            pen.width(line_heavy)
        else:
            if grid_shapes[r, c - 1] != grid_shapes[r, c]: pen.width(line_heavy)
        pen.forward(cell_draw_size)
    pen.left(90)
    pen.up()
    pen.forward(cell_draw_size)
    pen.right(90)
    pen.backward(cell_draw_size * num_rows)
    pen.down()

'''
def blank_out_cell(r,c):
    pen.setpos(start_coords[0]+r*cell_draw_size,start_coords[1]-c*cell_draw_size)
    pen.fillcolor("white")
    pen.setheading(0) #east
    pen.begin_fill()
    for i in range(4):
        pen.forward(cell_draw_size)
        pen.right(90)
    pen.end_fill() 
'''


# now numbers
pen.left(90)
pen.up()
pen.setpos(start_coords)
horiz_offset = cell_draw_size / 2
pen.forward(horiz_offset)  # centre horizontally
pen.right(90)
vert_offset = cell_draw_size * .9
pen.forward(vert_offset)  # vertical adjustment
pen.left(90)
for r in range(num_rows):
    for c in range(num_cols):
        if grid[r, c] != 0:
            pen.write(grid[r, c], align="center", font=("Arial", 20, "normal"))
        pen.forward(cell_draw_size)
    pen.right(90)
    pen.forward(cell_draw_size)
    pen.left(90)
    pen.backward(row_width + cell_draw_size)


'''
button1 = turtle.Turtle()
button1.hideturtle()
button1.shape('circle')
button1.fillcolor('red')
button1.penup()
button1.goto(150, 150)
button1.write("Click me!", align='center', font="(Arial,20)")
button1.sety(150)
#button.onclick(draw_onclick)
button1.showturtle()

button = turtle.Turtle()
button.hideturtle()
button.shape('circle')
button.fillcolor('red')
button.penup()
button.goto(200, 150)
button.write("22Click me!", align='center', font="(Arial,20)")
button.sety(150)
#button.onclick(draw_onclick)
button.showturtle()

'''

# input("presss enter to go further")


# SOLVING


stuck = False  # allow for constant loop so long as keep finding new numbers

while not stuck:

    found = 0
    # let's set this before any logic tests -- keep count of any new finds to see if stuck or carry on looping

    # Logic Test 1 - Simple - Check If Shape Has Just 1 Number missing
    for shape_number, shape in shape_coords.items():
        shape_size = len(shape)
        blank_cells = 0
        for cell in shape:
            if grid[cell] == 0:
                blank_cells += 1
                last_blank = cell
        if blank_cells == 1:
            found += 1
            # now let's work out what it should be
            numbers_needed = list(range(1, shape_size + 1))
            for cell in shape:
                if grid[cell] == 0:
                    blank_posn = cell
                else:
                    numbers_needed.remove(grid[cell])
            # numbers_needed[0] should now have the missing number
            missing_value = numbers_needed[0]
            print("missing", missing_value)
            print("cell location", blank_posn)
            grid[blank_posn] = missing_value
            display_newnumber(missing_value, blank_posn)
            found += 1
            # TODO -- array of which numbers are original


    # Logic Test 2 - Check if any cells have all but one number neighbouring
    for r in range(num_rows):
        for c in range(num_cols):
            if grid[r, c] == 0:  # only check for blanks
                numbers_available = list(range(1, 6))
                neighbours = get_neighbours(r, c)
                for nb in neighbours:
                    if grid[nb] in numbers_available:
                        numbers_available.remove(grid[nb])
                cells_in_this_shape = shape_coords[grid_shapes[r, c]]
                for cell in cells_in_this_shape:
                    if grid[cell] in numbers_available:
                        numbers_available.remove(grid[cell])
                if len(numbers_available) == 1:  # found one!
                    found += 1
                    grid[r, c] = numbers_available[0]
                    display_newnumber(numbers_available[0], (r, c), "green")

    # Logic Test 3 - Vicky's - Check how many places in a shape each number can go in
    for shape_number, shape in shape_coords.items():
        shape_size = len(shape)
        # we've got our shape, now let's go through each possible number
        for search_number in range(1, shape_size + 1):  # number we're looking for
            poss_cells = []  # keep tabs of how many solution cells
            already_there = False
            for cell in shape:
                if grid[cell] == search_number:
                    already_there = True
                    break
                elif grid[cell] == 0:
                    # let's see if this blank cell is allowed - check neighbours
                    neighbours = get_neighbours(*cell)  # *should split  tuple to send
                    neighbour_has = False
                    for nb in neighbours:
                        if grid[nb] == search_number:
                            neighbour_has = True
                            break
                    if not neighbour_has:  # not neighbouring - this cell ok
                        poss_cells.append(cell)
            # TODO - error handle if no places it can go
            if not already_there and len(poss_cells) == 1:
                # found one!
                found += 1
                grid[poss_cells[0]] = search_number
                display_newnumber(search_number, poss_cells[0], "magenta")

    # END OF SOLVING LOGIC -- and while loop
    if found == 0:
        stuck = True

if stuck:
    print("***LOOKS LIKE WE GOT STUCK***")

print(grid)

# ok, now let's try the pencil marks
def create_grid_pencils():
    grid_pencils = {}
    for r in range(num_rows):
        for c in range(num_cols):
            if grid[r, c] != 0:
                grid_pencils[r, c] = []
            else:
                # first find out which shape
                this_shape = grid_shapes[r, c]
                this_shape_coords = shape_coords[this_shape]
                shape_size = len(this_shape_coords)
                numbers_available = list(range(1, shape_size + 1))

                for cell in this_shape_coords:
                    # print ("*CELL*",cell)
                    if grid[cell] in numbers_available:
                        numbers_available.remove(grid[cell])

                neighbours = get_neighbours(r, c)
                for nb in neighbours:
                    if grid[nb] in numbers_available:
                        numbers_available.remove(grid[nb])

                grid_pencils[(r, c)] = numbers_available

    return (grid_pencils)


grid_pencils = create_grid_pencils()

def display_pencils(r, c, colour="gray"):
    vert_mini_offset = 0.33 * cell_draw_size
    xpos = start_coords[0] + cell_draw_size * c + horiz_offset
    ypos = start_coords[1] - cell_draw_size * r - vert_mini_offset  # down is negative
    pen.setpos(xpos, ypos)
    pen.color(colour)
    pencils = grid_pencils[r, c]
    # top row 1-2
    line = ""
    line += "1  " if 1 in pencils else "   "
    line += " 2" if 2 in pencils else "  "
    pen.write(line, align="center", font=("Arial", 8, "normal"))
    line = "3" if 3 in pencils else " "
    pen.setpos(xpos, ypos - vert_mini_offset)
    pen.write(line, align="center", font=("Arial", 8, "normal"))
    line = ""
    line += "4  " if 4 in pencils else "   "
    line += " 5" if 5 in pencils else "  "
    pen.setpos(xpos, ypos - 2 * vert_mini_offset)
    pen.write(line, align="center", font=("Arial", 8, "normal"))

    # print("number =", grid[r, c])
    # time.sleep(0.05)


def display_all_pencils(colour="gray"):
    for r in range(num_rows):
        for c in range(num_cols):
            if grid[r, c] == 0:
                display_pencils(r, c, colour)


display_all_pencils()


## START NEW LOOP HERE

stuck = False
use_intersection_elimination = True

while not stuck:
    found = 0

    # Logic #4: Something Cleverer
    # for each shape, go through each number one by one
    # which cells can hold that number
    # what are their neighbours
    # are any of those neighbours common to all of those cells
    # if so, that neighbour cannot hold that number

    if use_intersection_elimination:

        pencils_erased = 0
        debug_breakout = False
        for shape_number, shape in shape_coords.items():
            if debug_breakout: break
            shape_size = len(shape)
            for search_number in range(1, shape_size + 1):
                #print("shape", shape, "searchnum", search_number)
                if debug_breakout: break
                neighbours_to_check = ["not_started"]
                for cell in shape:
                    # print("-----",cell)
                    # print ("****",search_number,grid_pencils[cell])
                    if not neighbours_to_check: break  # if no intersection already, just skip
                    if search_number in grid_pencils[cell]:
                        neighbours = get_neighbours(*cell)
                        if neighbours_to_check == ["not_started"]:  # if this is the first
                            neighbours_to_check = neighbours
                            #print("search", search_number, "first n", neighbours_to_check)
                        else:
                            # we've got a list of neighbours, is there any overlap with neighbours to check so far
                            #print("subsq neighbours", neighbours)
                            new_nb = []
                            for nb in neighbours:
                                if nb in neighbours_to_check:
                                    new_nb.append(nb)
                            neighbours_to_check = new_nb
                            #print("intersect", neighbours_to_check)
                if neighbours_to_check:  # end of loop, not empty
                    if neighbours_to_check == ["not_started"]:
                        pass
                        #print("no neighbours - maybe number already in shape?")
                    else:
                        # this implies we can eliminate a value from a neighbour
                        #print("*Found a pencil to remove** ", neighbours_to_check, search_number)
                        for nb in neighbours_to_check:
                            #print("last cell=", cell, "neighbours to fix", nb, "number", search_number)

                            if search_number in grid_pencils[nb]:
                                #print("***REMOVING**")
                                pencils_erased += 1
                                # if pencils_erased>12: debug_breakout=True
                                display_pencils(*nb, colour="white")
                                #print("")
                                grid_pencils[nb].remove(search_number)
                                display_pencils(*nb, colour="red")
                            else:
                                pass
                                # something's gone wrong, but let's still carry on to see the grid
                                #print("no pencil found -- probably there's a full number there", nb, search_number)
                        #print("*have removed a pencil or found problem*")
                        # if cell[1]>7: debug_breakout=True
    use_intersection_elimination = False  #after used once, try without next loop round

    def tidy_pencils(found_number, r, c):
        # now erase pencils of that number from shape and neighbours
        this_shape = grid_shapes[r, c]
        this_shape_coords = shape_coords.get(this_shape)
        for cell in this_shape_coords:
            if found_number in grid_pencils[cell]:
                display_pencils(*cell, colour="white")
                grid_pencils[cell].remove(found_number)
                display_pencils(*cell)


        neighbours = get_neighbours(r, c)
        for nb in neighbours:
            if found_number in grid_pencils[nb]:
                display_pencils(*nb, colour="white")
                grid_pencils[nb].remove(found_number)
                display_pencils(*nb)


    # NEW LOGIC TEST - Now fill in cell where only one candidate (pencil number)
    for r in range(num_rows):
        for c in range(num_cols):
            pencils_here = grid_pencils[r, c]
            if len(pencils_here) == 1:
                found_number = pencils_here[0]
                display_pencils(r, c, colour="white")
                grid[r, c] = found_number
                grid_pencils[r, c] = []
                display_newnumber(found_number, (r, c), "orange")
                found += 1
                tidy_pencils(found_number, r, c)
    # TODO: fix that when new number found, pencils still showing up sometimes

    # NEW LOGIC TEST - check for shape with only one place that has a certain pencil number

    for shape_number, shape in shape_coords.items():
        shape_size = len(shape)
        for search_number in range(1, shape_size + 1):  # number we're looking for
            poss_cells = []  # keep tabs of how many solution cells
            #print(search_number, shape_number, shape)
            for cell in shape:

                if search_number in grid_pencils[cell]:
                    poss_cells.append(cell)

            if len(poss_cells) == 1:  # found a number
                found_cell = poss_cells[0]
                #print("**FOUND CELL", found_cell, search_number)
                display_pencils(*found_cell, colour="white")
                grid[found_cell] = search_number
                grid_pencils[found_cell] = []
                display_newnumber(search_number, found_cell, "red")
                found += 1
                tidy_pencils(search_number, *found_cell)

    # Got to end of loop
    if not found:
        if not use_intersection_elimination:
            use_intersection_elimination = True
            display_all_pencils("white")
        else:
            stuck = True

#print(grid_pencils)

turtle.done()

# pen.showturtle()


'''
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
'''
