# Grid Generate
""""
Suguru Puzzle Grid Generator -- trial

by Ashley,  April 2022
"""

import time, random    #, pprint, platform
import numpy as np
import pandas as pd
from pprint import pprint

import helper_functions

#global flags & variables

verbose = False
display_build = False
single_cell_stop = True


#set this outside __MAIN__ test to initialise
standard_shapes_tuple=[
        ('cross', [[0, 0], [1, -1], [1, 0], [1, 1], [2, 0]]),
        ('snake', [[0, 0], [0, 1], [0, 2], [1, -1], [1, 0]]),
        ('gun', [[0, 0], [0, 1], [0, 2], [0, 3], [1, 1]]),
        ('L', [[0, 0], [0, 1], [0, 2], [0, 3], [1, 0]]),
        ('T', [[0, 0], [0, 1], [0, 2], [1, 1], [2, 1]]),
        ('seahorse', [[0, 0], [0, 1], [1, -1], [1, 0], [2, 0]]),
        ('snail', [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1]]),
        ('S', [[0, 0], [0, 1], [1, 0], [2, -1], [2, 0]]),
        ('steps', [[0, 0], [0, 1], [1, -1], [1, 0], [2, -1]]),
        ('line-5', [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4]]),
        ('T-4', [[0, 0], [0, 1], [0, 2], [1, 1]]),
        ('L-4', [[0, 0], [0, 1], [0, 2], [1, 0]]),
        ('box-4', [[0, 0], [0, 1], [1, 0], [1, 1]]),
        ('snake-4', [[0, 0], [0, 1], [1, -1], [1, 0]]),
        ('line-4', [[0, 0], [0, 1], [0, 2], [0, 3]]),
        ('corner-3', [[0, 0], [0, 1], [1, 0]]),
        ('line-3', [[0, 0], [0, 1], [0, 2]]),
        ('line-2', [[0, 0], [0, 1]]),
        ('cell-1', [[0, 0]]),
        ('C-XX', [[0, 0], [0, 1], [0, 2], [1, 0], [1, 2]]),
        ('BigCorner-XX', [[0, 0], [0, 1], [0, 2], [1, 0], [2, 0]])
        ]

standard_shapes_long_as_list = [
    "cross", [[0, 0], [1, -1], [1, 0], [1, 1], [2, 0]],
    "snake", [[0, 0], [0, 1], [0, 2], [1, -1], [1, 0]],
    "gun", [[0, 0], [0, 1], [0, 2], [0, 3], [1, 1]],
    "L", [[0, 0], [0, 1], [0, 2], [0, 3], [1, 0]],
    "T", [[0, 0], [0, 1], [0, 2], [1, 1], [2, 1]],
    "seahorse", [[0, 0], [0, 1], [1, -1], [1, 0], [2, 0]],
    "snail", [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1]],
    "S", [[0, 0], [0, 1], [1, 0], [2, -1], [2, 0]],
    "steps", [[0, 0], [0, 1], [1, -1], [1, 0], [2, -1]],
    "line-5", [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4]],
    "T-4", [[0, 0], [0, 1], [0, 2], [1, 1]],
    "L-4", [[0, 0], [0, 1], [0, 2], [1, 0]],
    "box-4", [[0, 0], [0, 1], [1, 0], [1, 1]],
    "snake-4", [[0, 0], [0, 1], [1, -1], [1, 0]],
    "line-4", [[0, 0], [0, 1], [0, 2], [0, 3]],
    "corner-3", [[0, 0], [0, 1], [1, 0]],
    "line-3", [[0, 0], [0, 1], [0, 2]],
    "line-2", [[0, 0], [0, 1]],
    "cell-1", [[0, 0]],
    "C-XX", [[0, 0], [0, 1], [0, 2], [1, 0], [1, 2]],
    "BigCorner-XX", [[0, 0], [0, 1], [0, 2], [1, 0], [2, 0]],
]

def initialise_grid(rows,cols):
    global num_rows,num_cols
    num_rows=rows
    num_cols=cols
    create_blank_grids()



def random_colour():
    colour = "#"
    for i in range(3):
        colour = colour + hex(random.randint(155, 246))[-2:]
    return colour

def random_colour_stepped():
    colour = "#"
    step_size=10
    min_step=0
    max_step=4
    while True:
        colour = "#"
        steps=[]
        for i in range(3):
            steps.append(random.randint(0,4))
            colour = colour + hex(255-steps[i]*step_size)[-2:]
        #print("random colour steps", steps)
        if not (steps[0]==steps[1]==steps[2]):  #don't want grey
            #print(f"found - steps {steps}  hex {colour}")
            break
        #print("looping", steps)
    return colour

def random_colour_list(length=8):
    colour = "#"
    step_size = 10
    min_step = 0
    max_step = 4
    steps_list=[]
    colour_list=[]
    while len(steps_list)<length:
        while True:  #first find a non grey colour
            colour = "#"
            steps = []
            for i in range(3):
                steps.append(random.randint(0, 4))
                colour = colour + hex(255 - steps[i] * step_size)[-2:]
            #print("random colour steps", steps)
            if not (steps[0] == steps[1] == steps[2]):  # don't want grey
                #print(f"found - steps {steps}  hex {colour}")
                break
            #print("looping", steps)
        #now check against colours being 'too close' to each other (only 1 step away)
        too_close=False
        for steps_to_check in steps_list:
            comparison=0
            for i in range(3):
                comparison+=abs(steps[i]-steps_to_check[i])

            #print(comparison, steps, steps_to_check)
            if comparison<=1:
                too_close=True
                break
        if not too_close:
            steps_list.append(steps)
            colour_list.append(colour)

    return colour_list





def translated_shapes(shape_in):
        # work out rotations and reflections
        translations = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        shape_array = np.array(shape_in)
        my_array = shape_array.copy()
        my_array[:, 0], my_array[:, 1] = my_array[:, 1], my_array[:, 0].copy()  # this is to switch columns (ror rotation)
        shape_array_switched = my_array
        shapes_out = []

        # my_array[:, 0], my_array[:, 1] = my_array[:, 1], my_array[:, 0].copy()
        # we can do swap row and column which does some kind of ?rotate?

        for tr in translations:
            translated = (shape_array * tr).tolist()  # do the translation (reflection) first
            # now rebase the shape - find top left cell and make that 0,0
            translated.sort()
            first_coord = translated[0]
            translated = np.array(translated) - first_coord
            translated = translated.tolist()
            if translated not in shapes_out: shapes_out.append(translated)

            translated = (shape_array_switched * tr).tolist()  # now do rotation translation
            # now rebase the shape - find top left cell and make that 0,0
            translated.sort()
            first_coord = translated[0]
            translated = np.array(translated) - first_coord
            translated = translated.tolist()
            if translated not in shapes_out: shapes_out.append(translated)

            # res1tuple=[(i[0], i[1]) for i in res1]
            # shapes_out.append(res1tuple)
            # res2=(shape_array_switched * tr).tolist()
            # res2tuple=[(i[0], i[1]) for i in res1]
            # shapes_out.append(res2tuple)
            ##shapes_out.append((shape_array * tr).tolist())
            ##shapes_out.append((shape_array_switched * tr).tolist())
        return shapes_out

def next_free_space_spiral(start_coord):
    # this function spirals outwards from starting coord (r,c) until it finds an empty cell

    if grid_shapes[start_coord] == 0:
        return start_coord
        # if starting point already is blank

    move_coord_4 = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    new_point = start_coord
    step_size = 0

    for i in range(max(num_cols, num_rows)):
        any_in_bounds = False
        for move in move_coord_4:
            if move[0] == 0:
                step_size += 1  # increase step size every other step, that seems to make a spiral
            for steps in range(step_size):

                new_point = add_coords(new_point, move)
                if in_bounds(new_point):
                    any_in_bounds = True
                    if grid_shapes[new_point] == 0:
                        return new_point

        if not any_in_bounds:
            return None  # spiral reached outside so stop

def gen_predet_shapes(turtle_fill=True,shuffle_slightly=False,shuffle_at_start=False, funky_shuffle=True, single_cell_upper_limit=3):
    global start_point, move_coord, count, val, shape, shape_number, new_point, move, shape_permutations, valid, colour, num_rows,num_cols
    # set start coordinates
    # start_point = (int(num_rows / 2), int(num_cols / 2))
    # start_point = (random.randint(0,num_rows-1),random.randint(0,num_cols-1))
    # normal random choice
    start_point = (
    random.randint(num_rows // 3 - 1, num_rows * 2 // 3 - 1), random.randint(num_cols // 3 - 1, num_cols * 2 // 3 - 1))
    # biased to middle third
    move_coord = [(0, 1), (1, 0), (0, -1), (-1, 0), (0, 0)]


    single_cell_max = random.randint(0, single_cell_upper_limit)

    defined_shapes_to_choose = []  # let's try a list of lists, at least that's got a defined order
    #TODO - at least make this happen once not every loop
    for count, val in enumerate(standard_shapes_long_as_list):
        if count % 2 == 0:
            shape = [val]

        else:
            shape.append(val)
            defined_shapes_to_choose.append(shape)
    p1 = defined_shapes_to_choose.pop()
    p2 = defined_shapes_to_choose.pop()
    # pop last two are fatal
    # TODO - deal with those differently  --- need to pop even if not print
    # TODO - better have 6 separate lists  5,4,3,2,1 shapes and then fatal shape - and then combine as needed, or randomise parts as needed
    # print (defined_shapes_to_choose)

    if shuffle_at_start:
        shapes_to_shuffle=defined_shapes_to_choose[:10] #5 cell  shapes only
        random.shuffle(shapes_to_shuffle)
        print("shuffle at start:",shapes_to_shuffle)
        defined_shapes_to_choose_shuffled=shapes_to_shuffle+defined_shapes_to_choose[10:]
        print(defined_shapes_to_choose_shuffled)

    else:
        defined_shapes_to_choose_shuffled = defined_shapes_to_choose[:]



    # todo - why isn't this printing?
    # TODO - plus now need to stop when finished and also add some randomness
    go = 1
    shape_number = 1

    single_cell_count=0




    finished = False
    for loops in range(50):  # was 500 -- stopping to try spiral
        # ##THIS LOOP WRONG!!  only need to loop multi times to find a starting point - not to choose shapes [we go through every possible shape permutation after all]
        #TODO: this should really be a While loop --- shouldn't need to keep trying if done correctly

        # choose a direction to go

        if verbose: print(go)
        if display_build: time.sleep(.02)
        if go == 1:
            new_point = start_point
            # print ("first =",new_point)
            go += 1

        else:
            go += 1
            # choose where to move next
            random_move = True #False
            if random_move:
                move = random.choice(move_coord)
                pot_new_point = add_coords(move, new_point)
                if in_bounds(pot_new_point):
                    new_point = pot_new_point
                    #print("grid value:",grid[new_point])
                else:
                    pass
                    #print ("out of bounds")
                    #continue  # meaning restart the loop as out of bounds -- don't do this now using spiral immediately after
            if True:  # try spiral move in all cases whatever
                if random.random()<.3:
                    spiral_point = next_free_space_spiral(new_point)
                else:
                    spiral_point = next_free_space_spiral(start_point)
                if verbose: print(f"spiral point {spiral_point} -- original in {new_point}")
                if spiral_point:
                    new_point = spiral_point
                else:
                    # spiral has run out -- hopefully because we've filled the whole thing!
                    if verbose: print("*filled the grid*")
                    finished = True
                    break

        #location to solve now set
        if verbose:
            print ("Solve Point: ",new_point)
            if grid_shapes[new_point]:
                print ("*****grid occupied there *****###")

        if not finished:
            # random choice whether to shuffle or use preferred order
            # TODO -- when randomly shuffling the shape order, first shuffle the 5 length shapes they should still be preferred before the others

            if funky_shuffle:
                random_threshold=0.15
                if defined_shapes_to_choose_shuffled[0][0] in ["cross","steps","snake"]:
                    random_threshold=0.8
                elif defined_shapes_to_choose_shuffled[0][0] in ["gun","seahorse"]:
                    random_threshold = 0.5
                #print(defined_shapes_to_choose_shuffled[0][0],random_threshold)

                if random.random()>random_threshold:  #shuffle if higher than threshold
                    shapes_to_shuffle = defined_shapes_to_choose[:10]  # 5 cell  shapes only
                    random.shuffle(shapes_to_shuffle)
                    #print(shapes_to_shuffle)
                    defined_shapes_to_choose_shuffled = shapes_to_shuffle + defined_shapes_to_choose[10:]
                    #print(defined_shapes_to_choose_shuffled)

            if shuffle_slightly:
                if random.random()<0.1:
                    defined_shapes_to_choose_shuffled = defined_shapes_to_choose.copy()
                    shuffle_number=random.randint(1,7)
                    #print ("start",len(defined_shapes_to_choose_shuffled))
                    #pprint(defined_shapes_to_choose_shuffled)
                    shape_to_swap=defined_shapes_to_choose_shuffled.pop(shuffle_number)
                    print(shape_to_swap)
                    defined_shapes_to_choose_shuffled.insert(0,shape_to_swap)
                    #print("switched",len(defined_shapes_to_choose_shuffled))
                    #pprint(defined_shapes_to_choose_shuffled)

            # elif random.random() < 1:
            #     defined_shapes_to_choose_shuffled = defined_shapes_to_choose[:]
            # else:
            #     random.shuffle(defined_shapes_to_choose_shuffled)


            for shape_name, base_shape in defined_shapes_to_choose_shuffled:
                # shape_to_try = [[0, 0], [1, -1], [1, 0], [1, 1], [2, 0]]
                if verbose: print("*****SHAPE:", shape_name)

                # TODO: we're going to need all the translations of the shape to try
                shape_permutations = translated_shapes(base_shape)
                shuffled_shape_rotation=True
                if shuffled_shape_rotation:
                    random.shuffle(shape_permutations)
                    #shuffle permutations so the shapes don't tend to completely align automatically

                for shape_to_try in shape_permutations:
                    if verbose: print(shape_to_try)

                    # TODO -- add in the full set of shapes ///surely I have haven't i?

                    for home_coord in shape_to_try:
                        # now alter which cell of the shape is the one to line up  on the starting cell
                        home_coord_offset = (-home_coord[0], -home_coord[1])
                        if verbose: print("home coord offset =", home_coord_offset)

                        # try to add it in
                        valid = True
                        for coord in shape_to_try:
                            adjusted_coord = add_coords(coord, new_point, home_coord_offset)
                            if verbose: print(adjusted_coord)
                            if not in_bounds(adjusted_coord):
                                valid = False
                                break

                            if grid_shapes[adjusted_coord] != 0:  # already occupied
                                valid = False
                                break

                        #last test - does it create a blocked off single cell (this is generally a bad thing)
                        #what's the logic for this?
                        #for every cell in the new shape, work out what are the "affected cells" - ie those that are directly adjacent (not diagonal)
                        #then for every affected cell, see if it is blank and see if its own direct sideways neighbours are completely blocked by existing or this new shape
                        #ideally if already blocked, then this is already a problem - leave it be
                        #so long as at least one sideways escape route, that's ok
                        #otherwise fail this shape


                        if single_cell_stop:
                            if valid:
                                #first establish affected cells
                                affected_cells=set()
                                shape_try_adjusted=[]
                                for coord in shape_to_try:
                                    adjusted_coord = add_coords(coord, new_point, home_coord_offset)
                                    shape_try_adjusted.append(adjusted_coord)
                                    affected_cells.update(get_sideways_neighbours(adjusted_coord))

                                for coord in affected_cells:
                                    if coord not in shape_try_adjusted and grid_shapes[coord]==0: #don't check members of prospective shape itself and affected cell needs to be empty
                                        sideways_neighbours=get_sideways_neighbours(coord)
                                        empty_before_shape=0
                                        empty_after_shape=0
                                        #logic that follows - we need affected shapes to have at least 1 blank - after the shape has gone in (if had 0 before that's ok)
                                        for nb in sideways_neighbours:
                                            if grid_shapes[nb]==0:
                                                empty_before_shape+=1
                                                if nb not in shape_try_adjusted:
                                                    empty_after_shape+=1
                                        if empty_after_shape==0 and empty_before_shape!=0:
                                            single_cell_count+=1
                                            if single_cell_count>single_cell_max:  #allow *some*
                                                #TODO check how close?
                                                valid=False
                                                #print (f"**single cell**  affected cell {coord} -- emptybefore  {empty_before_shape}  emptyafter {empty_after_shape}")
                                                break

                                #print (f"shape number {shape_number}-- valid {valid} -- shape coords {shape_try_adjusted} ** affected cells: {affected_cells}")




                        if valid: break
                    if valid: break
                if valid: break

            # if valid, add in and update records
            if valid:
                colour = random_colour_stepped()
                for coord in shape_to_try:
                    adjusted_coord = add_coords(coord, new_point, home_coord_offset)
                    grid_shapes[adjusted_coord] = shape_number
                    if turtle_fill:
                        fill_cell(adjusted_coord, colour)
                if verbose: print("valid shape")
                shape_number += 1

            # if it fails loop back to try a different shape
            else:
                #if verbose: print(f"not found valid shape possibility, coord={new_point}")
                print(f"not found valid shape possibility, coord={new_point}")   #this shouldn't really happen should it?





def add_coords(coord1, coord2,offset=(0,0)):
    return (coord1[0] + coord2[0] + offset[0], coord1[1] + coord2[1] + offset[1])


def display_numbers(zero_override=None):
    screen.tracer(1)
    pen.left(90)
    pen.up()
    pen.setpos(start_coords)
    horiz_offset = cell_draw_size / 2
    vert_offset = cell_draw_size * .9
    pen.forward(horiz_offset)  # centre horizontally
    pen.right(90)
    screen.tracer(0)

    pen.forward(vert_offset)  # vertical adjustment
    pen.left(90)
    for r in range(num_rows):
        for c in range(num_cols):
            if grid[r, c] != 0:
                pen.write(grid[r, c], align="center", font=("Arial", 20, "normal"))
            elif zero_override:
                pen.write(zero_override, align="center", font=("Arial", 20, "normal"))

            pen.forward(cell_draw_size)
        pen.right(90)
        pen.forward(cell_draw_size)
        pen.left(90)
        pen.backward(row_width + cell_draw_size)

    screen.tracer(0)

def in_bounds(coord):
    valid = (0 <= coord[0] <= num_rows - 1) and (0 <= coord[1] <= num_cols - 1)
    return valid


def create_blank_grids(values_only=False):
    global grid, grid_shapes
    grid = np.zeros((num_rows, num_cols), dtype=int)
    if not values_only:
        grid_shapes = np.zeros((num_rows, num_cols), dtype=int)

def array2string(array_in):
    return np.array2string(array_in)


def get_shape_coords():
    global shape_coords, r, c, this_shape
    shape_coords = {}
    for r in range(num_rows):
        for c in range(num_cols):
            this_shape = grid_shapes[r, c]
            this_shape_coords = shape_coords.get(this_shape)
            if not this_shape_coords:
                this_shape_coords = []
            this_shape_coords.append((r, c))
            shape_coords[this_shape] = this_shape_coords

    return shape_coords


def get_neighbours(r, c):
    neighbours = []
    for nb_r in range(r - 1, r + 2):
        if 0 <= nb_r <= num_rows - 1:
            for nb_c in range(c - 1, c + 2):
                if 0 <= nb_c <= num_cols - 1:
                    neighbours.append((nb_r, nb_c))
    neighbours.remove((r, c))  # don't include itself
    return neighbours

def get_sideways_neighbours(coord):
    #ie no diagonals
    r,c = coord
    neighbours = []
    for nb_r in range(r - 1, r + 2,2):  #hopefully the 2 will skip over itself
        if 0 <= nb_r <= num_rows - 1:
            neighbours.append((nb_r, c))
    for nb_c in range(c - 1, c + 2,2):
        if 0 <= nb_c <= num_cols - 1:
            neighbours.append((r, nb_c))
    return neighbours


def real_iterate(timeout=None):
    # really iterate , not just recursive
    global iterate_number_count, iterate_cell_count, max_iters
    if timeout:
        timeout_time=time.time()+timeout
    success = False
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
                if verbose:
                    if iterate_cell_count % 50000 == 0:
                        elapsed = time.time() - start_time
                        if not elapsed:
                            rate = 0
                        else:
                            rate = iterate_cell_count / elapsed
                        print("iterate counts", iterate_cell_count, iterate_number_count, "cell", cell_iter_no,
                              "time", elapsed, "rate", rate)
            else:
                # got as far as end cell - complete
                #print("*complete*")
                success = True
                break

        if next_step == "descend":
            grid[rc] = 0
            cell_iter_no -= 1
            if cell_iter_no < 0:
                next_step = "FAIL"
                break

        rc = row_col[cell_iter_no]
        # print ("rc",rc)

        if next_step == "ascend" or next_step == "starting":
            max_nums, shapes = iter_shapes[cell_iter_no]
            nums_avail = list(range(1, max_nums + 1))
            for shape in shapes:
                this_num = grid[shape]
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

            grid[rc] = num_to_try
            iterate_number_count += 1
            # now let's check if valid
            valid = True
            neighbours = iter_nonshape_neighbours[cell_iter_no]
            for nb in neighbours:
                if grid[nb] == num_to_try:
                    valid = False
                    break

            # if ok - ascend a level in iteration
            if valid:
                if timeout:
                    ok_continue=(time.time()<timeout_time)
                else:
                    ok_continue=(iterate_cell_count<max_iters)
                timed_out=not ok_continue
                if cell_iter_no < num_rows * num_cols - 1 and ok_continue:
                    iterate_cell_count += 1
                    next_step = "ascend"
                    if iterate_cell_count % 10000 == 0:
                        elapsed = time.time() - start_time
                        if not elapsed:
                            rate = 0
                        else:
                            rate = iterate_cell_count / elapsed
                        print("iterate counts", iterate_cell_count, iterate_number_count, "time", elapsed,
                              "rate", rate)

            else:
                # doesn't work try next number
                next_step = "inc_number"
                grid[rc] = 0

        # this is end of while loop I think

    # print(grid)
    # END OF ITERATION

    return success, timed_out

def find_least_possible_values():
    '''
    returns dictionary of grid possibles, plus the location of cell with least possibles
    '''
    #was create_grid_pencils in the earlier suguru file
    grid_possibles = {}
    min_possibles=99
    min_location=[]
    for r in range(num_rows):
        for c in range(num_cols):
            if grid[r, c] != 0:
                grid_possibles[r, c] = []
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

                grid_possibles[(r, c)] = numbers_available
                possibles_count=len(numbers_available)
                if possibles_count<min_possibles:
                    min_possibles=possibles_count
                    min_location=(r,c)

    return (grid_possibles,min_location)

def recalc_one_cell_possibles(coord):
    r,c=coord
    this_shape = grid_shapes[r, c]
    this_shape_coords = shape_coords[this_shape]
    shape_size = len(this_shape_coords)
    numbers_available = list(range(1, shape_size + 1))

    for cell in this_shape_coords:
        if grid[cell] in numbers_available:
            numbers_available.remove(grid[cell])

    neighbours = get_neighbours(r, c)
    for nb in neighbours:
        if grid[nb] in numbers_available:
            numbers_available.remove(grid[nb])

    return numbers_available


def find_least_possible_values2():
    global linked_cells_lookup
    #was create_grid_pencils in the earlier suguru file
    #but now has pre-calculated list of linked cells


    grid_possibles = {}
    min_possibles=99
    min_location=[]
    for r in range(num_rows):
        for c in range(num_cols):
            if grid[r, c] != 0:
                grid_possibles[r, c] = []
            else:
                #use lookup
                linked_cells, numbers_available_ref = linked_cells_lookup[(r,c)]
                numbers_available=numbers_available_ref.copy()

                # first find out which shape
                # this_shape = grid_shapes[r, c]
                # this_shape_coords = shape_coords[this_shape]
                # shape_size = len(this_shape_coords)
                # numbers_available = list(range(1, shape_size + 1))

                for cell in linked_cells:
                    # print ("*CELL*",cell)
                    if grid[cell] in numbers_available:
                        numbers_available.remove(grid[cell])

                grid_possibles[(r, c)] = numbers_available
                possibles_count=len(numbers_available)
                if possibles_count<min_possibles:
                    min_possibles=possibles_count
                    min_location=(r,c)


    return (grid_possibles,min_location)


def real_iterate_least(timeout=None):
    # trying version of real iterate which chooses the cell to iterate based on which has least options
    global iterate_number_count, iterate_cell_count, max_iters
    if timeout:
        timeout_time=time.time()+timeout
    success = False
    numbers_to_try_stack = {}
    cell_iter_no = 0
    keep_iterating = True
    timed_out = False
    next_step = "starting"
    cells_tried_stack={}
    while keep_iterating:
        # let's start loop off
        # print("next step",next_step)
        if next_step == "ascend":
            if cell_iter_no < num_rows * num_cols - 1:  # TODO create variable
                cell_iter_no += 1
                iterate_cell_count += 1

            else:
                # got as far as end cell - complete
                #print("*complete*")
                success = True
                break

        if next_step == "descend":
            grid[rc] = 0
            cell_iter_no -= 1
            if cell_iter_no < 0:
                next_step = "FAIL"
                break

        #rc = row_col[cell_iter_no]
        # print ("rc",rc)
        grid_possibles,least_possible = find_least_possible_values()
        #print (cell_iter_no,least_possible,iterate_cell_count,grid_possibles)

        if next_step == "ascend" or next_step == "starting":
            #find the next cell to try -- this time by finding cell with least possibilities

            rc=least_possible
            nums_avail = grid_possibles[rc]
            numbers_to_try_stack[cell_iter_no] = nums_avail
            cells_tried_stack[cell_iter_no]= rc


        elif next_step == "descend":
            #max_nums, shapes = iter_shapes[cell_iter_no]  # TODO do we need shapes now?
            nums_avail = numbers_to_try_stack[cell_iter_no]
            rc = cells_tried_stack[cell_iter_no]

        # now we actually iterate do we?
        # print ("where we're at",cell_iter_no,nums_avail)

        if not nums_avail:
            # run out of numbers for cell, retreat
            next_step = "descend"
        else:
            num_to_try = nums_avail.pop(0)
            numbers_to_try_stack[cell_iter_no] = nums_avail
            grid[rc] = num_to_try

            #SKIPPING this bit - as we already have weeded down to only legit numbers to choose


            # iterate_number_count += 1
            # # now let's check if valid
            valid = True
            # neighbours = iter_nonshape_neighbours[cell_iter_no]
            # for nb in neighbours:
            #     if grid[nb] == num_to_try:
            #         valid = False
            #         break

            # if ok - ascend a level in iteration
            if valid:
                if timeout:
                    ok_continue=(time.time()<timeout_time)
                else:
                    ok_continue=(iterate_cell_count<max_iters)
                timed_out=not ok_continue

                if cell_iter_no < num_rows * num_cols - 1 and ok_continue:
                    #iterate_cell_count += 1
                    next_step = "ascend"


            else:
                # doesn't work try next number
                next_step = "inc_number"
                print ("*******SHOULDN'T BE HERE********")
                grid[rc] = 0

        # this is end of while loop I think

    # print(grid)
    # END OF ITERATION

    return success, timed_out

def BROKEN_real_iterate_least2(timeout=None):
    #this doesn't work, but am going to try refactoring a new version instead
    #commit called "iterate 2 - slightly faster" has a version that is still working
    ##########
    # trying version of real iterate which chooses the cell to iterate based on which has least options
    global iterate_number_count, iterate_cell_count, max_iters, linked_cells_lookup
    if timeout:
        timeout_time=time.time()+timeout
    success = False
    numbers_to_try_stack = {}
    cell_iter_no = 0
    keep_iterating = True
    timed_out = False
    next_step = "starting"
    cells_tried_stack={}

    ##let's precalculate all the cell addresses that are linked to any individual cell
    # so a combo of cells in the same shape and neighbours (de-duplicated)


    linked_cells_lookup={}

    for r in range(num_rows):
        for c in range(num_cols):

            #start with neighbours
            these_linked_cells = get_neighbours(r, c)

            # now add non duplicate cells from shape
            this_shape = grid_shapes[r, c]
            this_shape_coords = shape_coords[this_shape]
            numbers_available = list(range(1,len(this_shape_coords)+1))

            for cell in this_shape_coords:
                if cell not in these_linked_cells and cell!=(r,c):
                    these_linked_cells.append(cell)

            linked_cells_lookup[(r,c)]=(these_linked_cells,numbers_available)

    print (linked_cells_lookup)


    while keep_iterating:
        # let's start loop off
        # print("next step",next_step)
        if next_step == "ascend":
            if cell_iter_no < num_rows * num_cols - 1:  # TODO create variable
                cell_iter_no += 1
                iterate_cell_count += 1

            else:
                # got as far as end cell - complete
                #print("*complete*")
                success = True
                break

        if next_step == "descend":
            grid[rc] = 0
            cell_iter_no -= 1
            if cell_iter_no < 0:
                next_step = "FAIL"
                break

        #rc = row_col[cell_iter_no]
        # print ("rc",rc)
        if next_step=="descend" or next_step=="starting":
            grid_possibles,least_possible = find_least_possible_values2()
        #print ("#",cell_iter_no,"LP:",least_possible,"Count:",iterate_cell_count,grid_possibles)

        if next_step == "ascend" or next_step == "starting":
            #find the next cell to try -- this time by finding cell with least possibilities
            rc=least_possible
            print (f"rc  {rc}, cell iter no {cell_iter_no}, next step {next_step}")
            nums_avail = grid_possibles[rc]
            numbers_to_try_stack[cell_iter_no] = nums_avail
            cells_tried_stack[cell_iter_no]= rc


        elif next_step == "descend":
            #max_nums, shapes = iter_shapes[cell_iter_no]  # TODO do we need shapes now?
            nums_avail = numbers_to_try_stack[cell_iter_no]
            rc = cells_tried_stack[cell_iter_no]

        # now we actually iterate do we?
        # print ("where we're at",cell_iter_no,nums_avail)

        if not nums_avail:
            # run out of numbers for cell, retreat
            next_step = "descend"
        else:
            num_to_try = nums_avail.pop(0)
            numbers_to_try_stack[cell_iter_no] = nums_avail
            grid[rc] = num_to_try   #**TRY THE NUMBER

            ##now update the possibles
            linked_cells=linked_cells_lookup[(r,c)][0]
            print (linked_cells)
            min_possibles=99
            min_location=[]
            for cell in linked_cells:
                print (f"cell {cell} ;;  {r},{c}")
                if grid[cell] in grid_possibles[r,c]:
                    grid_possibles.remove(grid[cell])
                if len(grid_possibles[r,c])<min_possibles:
                    min_possibles=len(grid_possibles[r,c])
                    min_location=(r,c)

            least_possible=min_location
            print (f"done least possible: {least_possible}")



            #print (grid)

            #SKIPPING this bit - as we already have weeded down to only legit numbers to choose


            # iterate_number_count += 1
            # # now let's check if valid
            valid = True
            # neighbours = iter_nonshape_neighbours[cell_iter_no]
            # for nb in neighbours:
            #     if grid[nb] == num_to_try:
            #         valid = False
            #         break

            # if ok - ascend a level in iteration
            if valid:
                if timeout:
                    ok_continue=(time.time()<timeout_time)
                else:
                    ok_continue=(iterate_cell_count<max_iters)
                timed_out=not ok_continue

                if cell_iter_no < num_rows * num_cols - 1 and ok_continue:
                    #iterate_cell_count += 1
                    next_step = "ascend"


            else:
                # doesn't work try next number
                next_step = "inc_number"
                print ("*******SHOULDN'T BE HERE********")
                grid[rc] = 0

        # this is end of while loop I think

    # print(grid)
    # END OF ITERATION

    return success, timed_out


def create_linked_cells_lookup():
    linked_cells_lookup={}

    for r in range(num_rows):
        for c in range(num_cols):

            #start with neighbours
            these_linked_cells = get_neighbours(r, c)

            # now add non duplicate cells from shape
            this_shape = grid_shapes[r, c]
            this_shape_coords = shape_coords[this_shape]
            #numbers_available = list(range(1,len(this_shape_coords)+1))

            for cell in this_shape_coords:
                if cell not in these_linked_cells and cell!=(r,c):
                    these_linked_cells.append(cell)

            linked_cells_lookup[(r,c)]=(these_linked_cells)  #,numbers_available)

    return linked_cells_lookup

def find_least_possibles(grid_possibles):
    min_possibles = 99
    min_location = None
    for r in range(num_rows):
        for c in range(num_cols):
            if grid[r,c]==0: #only check non-solved  cells
                if len(grid_possibles[r,c])<min_possibles:
                    min_possibles=len(grid_possibles[r,c])
                    min_location=(r,c)
    return min_location


def is_grid_legit():
    ''' assume grid has been set with values, check it's a valid solution - ie nothing broken'''
    for r in range(num_rows):
        for c in range(num_cols):
            this_value=grid[r,c]
            this_shape = grid_shapes[r, c]
            this_shape_coords = shape_coords[this_shape]
            for coord in this_shape_coords:
                if grid[coord]==this_value and coord!=(r,c):
                    return False
            for coord in get_neighbours(r,c):
                if grid[coord]==this_value and coord!=(r,c):
                    return False

    return True


def do_absolutely_nothing_just_to_test():
    pass

def new_iterate(timeout=5,always_wholegrid_least=False,single_location_checker=False,debug=False):
    '''

    :param always_wholegrid_least:  do you want to check each iteration what least possibles are across whole grid? if False just check within cells most recently linked to cell iterated
    :return: success, no of iterations
    '''

    #print ("********START NEW ITERATE*******")

    time_started=time.time()

    #initialise variables, pointers and stacks
    max_cells=num_rows*num_cols-1  #target for final iteration
    iteration_pointer=0  # how far up in the cells we are - goes up and down and maxes out at max cells
    iteration_cycles_counter=0  #count how many goes we need - keeps going up

    iteration_cells_used_stack={}
    values_changed_stack={}

    # create lookup of all linked cells and list of max possible values
    linked_cells_lookup=create_linked_cells_lookup()
    # calc possible values of entire grid [existing function]
    grid_possibles,least_possible_location=find_least_possible_values()  #use original v1 to start as not bothering with lookup if only using ths once
    live_cell = least_possible_location

    #Now starting iteration loop
    ni_debug=False #False #True
    # if single_location_checker:
    #     ni_debug=True
    if debug:  ni_debug=True


    while True:   #permanent loop - normally exit via return statements

        # ##Assume starting a new cell -- actually no- this could be same cell next number
        iteration_cycles_counter+=1

        #do_absolutely_nothing_just_to_test()

        # what values are possible for this cell
        possibles_here=grid_possibles[live_cell]

        if iteration_cycles_counter%2500==0:
            #print (f"#{iteration_cycles_counter:,}")
            if timeout:
                if time.time()>time_started+timeout:
                    #Timed Out
                    return "timed out",iteration_cycles_counter



        if ni_debug:
            print (f"#{iteration_cycles_counter}, itno {iteration_pointer}, live cell {live_cell}, possibles {possibles_here}")
            #print("4/9??", grid_possibles[4,9])
        #print(values_changed_stack)

        # first check if no values left - if so skip and go down
        if possibles_here:  #ok, so there are some, carry on
            # pull a value
            value_to_use=possibles_here.pop(0)
            if ni_debug: print ("value to use:", value_to_use)

            # set grid with this value
            grid[live_cell]=value_to_use

            # if this was the last cell -- exit as successful
            if iteration_pointer==max_cells:
                # print ("SUCCESS")
                return "success", iteration_cycles_counter

            # look up linked cells
            linked_cells_here=linked_cells_lookup[live_cell]

            # Linked Cell loop -- for every linked cell - save status first and then change if has same number
            shapes_changed=set()
            before_changes_dict={}
            for linked_cell in linked_cells_here:
                # first, what *were* the possibilities before changing -- build list of coordinates and possibilities, to save to stack

                if grid[linked_cell]==0:
                    # (only need to do for unsolved cells)
                    this_link_possibilities=grid_possibles[linked_cell]
                    before_changes_dict[linked_cell]=this_link_possibilities.copy() #try a copy so it doesn't keep changing afterwards

                    # now check impact
                    # update possibilities - remove current value if appears there
                    if value_to_use in this_link_possibilities:
                        this_link_possibilities.remove(value_to_use)
                        #this is effectively a pointer, so changes the main grid_possibles too
                        shapes_changed.add(grid_shapes[linked_cell])  #it's a set, so no duplicates




            #Now doing after the linked cells loop
            ######***MOVE THIS INTO A FUNCTION
            #extra bit - check if after changes we're  leaving any possible number only in one place in shape
            #if so, make that the only possibility in that cell
            #mirrors the human logic solver

            if single_location_checker: #one_per_shape:
                #print ("itno",iteration_cycles_counter,"shapes changed",shapes_changed)
                for this_shape in shapes_changed:

                    this_changed_shape_coords=shape_coords[this_shape]
                    #print(f"live cell {live_cell}  [shape {grid_shapes[live_cell]}], linked_cell {linked_cell}, this_shape {this_shape}, coords {this_changed_shape_coords}")

                    numbers_to_check=range(1, len(this_changed_shape_coords) + 1)
                    for number in numbers_to_check:
                        #print ("n2c -",number)
                        places_found=[]
                        #print ("TCS", this_changed_shape_coords)
                        for cell in this_changed_shape_coords:
                            if grid[cell]==0:
                                #only check non solved cells
                                #print (number, cell, grid_possibles[cell])
                                if number in grid_possibles[cell]:
                                    places_found.append(cell)
                                    if len(places_found)>1:
                                        #print("at least 2")
                                        break
                        if len(places_found)==1:
                            # good, we've found a cell that's the only location for a number within a shape
                            single_location_left=places_found[0]
                            #let's just check if it's already the *only* possible there - if so, it's already being dealt with
                            if len(grid_possibles[single_location_left])>1:

                                #if that location not already in linked cells (eg if in wider shape) - add to changed shapes before changing
                                # print("this linked cell",linked_cell,"linkedcellshere",linked_cells_here)
                                # print(f"single location left {single_location_left}",before_changes_dict)
                                # print (before_changes_dict)
                                if single_location_left not in before_changes_dict:
                                    before_changes_dict[single_location_left]=grid_possibles[single_location_left].copy()

                                # print(before_changes_dict)

                                # print(grid_possibles[places_found[0]])
                                grid_possibles[places_found[0]]=[number]
                                # print ("Done it",places_found[0],"itno",iteration_cycles_counter)
                                # print (grid_possibles[places_found[0]])



            ##PREPARE TO GO UP AN ITERATION LEVEL
            if ni_debug:print (grid)

            if always_wholegrid_least==True or iteration_pointer<10:
                #if this flag set, every iteration check the full grid for what cell next has least no of possibles
                #also if iteration pointer lower than small number -- first few iterations useful to jump about
                next_cell = find_least_possibles(grid_possibles)
            else:
                #in this case just find fewest possibles in linked_cells - those we've just changed
                #**actually this was wrong -- need to check what the linked cells are NOW - after we've changed

                least_possibles=99
                for cell in before_changes_dict.keys():
                    possibles_here=grid_possibles[cell]
                    if len(possibles_here)<least_possibles:
                        least_possibles=len(possibles_here)
                        least_possible_location=cell

                if least_possibles<99:
                    next_cell = least_possible_location
                    if always_wholegrid_least=="hybrid":
                        if least_possibles>1:
                            #check if better off using full width least possibles
                            alt_location=find_least_possibles(grid_possibles)
                            #print (iteration_cycles_counter,least_possibles,len(grid_possibles[alt_location]))
                            if len(grid_possibles[alt_location])<least_possibles:
                                next_cell=alt_location  #override





                else:
                    #ok, so this time we've run out of things to change so have to do the full grid find least possibles anyway
                    next_cell = find_least_possibles(grid_possibles)

            if len(grid_possibles[next_cell]):  #check, as no point in going up if going to come down again straight away

                # push current cell coordinates to stack
                iteration_cells_used_stack[iteration_pointer]=live_cell

                if next_cell not in before_changes_dict:
                    before_changes_dict[next_cell]=grid_possibles[next_cell].copy()
                    #if next cell wasn't already one we'd changed, then save it into stack anyway

                # push updated cells (linked cells) to stack  -- this is their original value before change
                if ni_debug: print (f"Saving: IP {iteration_pointer},  {before_changes_dict}")
                # print()
                values_changed_stack[iteration_pointer]=before_changes_dict
                # [push remaining values for this cell to stack -- do we need to?? GUESSING NO]

                #set new coord, increment counter
                live_cell=next_cell
                iteration_pointer+=1
                # continue loop -- skipping over the going down bit
                continue

            else:
                #need to reset the cells we've changed because we're not going up, as otherwise that won't happen
                for cell,possibles_here in before_changes_dict.items():
                    grid_possibles[cell]=possibles_here
                if ni_debug: print ("**skipping going up to no-possibles cell -- ",next_cell)


        ##***ARRIVING HERE (beyond continue) means there were no possibles
        # ##prepare to go down
        # if no cells left -- exit as failure
        if iteration_pointer==0:
            #print ("FAIL - no cells left")
            return "failed", iteration_cycles_counter
        # decrease counter
        iteration_cells_used_stack[iteration_pointer]="--"  #blank out - don't really need to
        iteration_pointer-=1
        #reset grid value back to 0 - unsolved
        grid[live_cell]=0
        # pull coord from stack - back to where we were last time - this is new coord
        last_live_cell=live_cell
        live_cell=iteration_cells_used_stack[iteration_pointer]

        # pull original coords + values of linked cells from stack
        before_changes_dict=values_changed_stack[iteration_pointer]
        #print(before_changes_dict)
        # reset those cells in possibles list back to original state
        for cell,possibles_here in before_changes_dict.items():
            grid_possibles[cell]=possibles_here


        ##shouldn't need this now -- have found a way to add it in to the dictionary
        if last_live_cell not in before_changes_dict:
            grid_possibles[last_live_cell]=recalc_one_cell_possibles(last_live_cell)
            if ni_debug: print ("**MISSING CELL INFO**", last_live_cell, grid_possibles[last_live_cell])

        # continue loop


    #debug -- check against full calculated set of grid possibles
    # full_calc_possibles,least_val=find_least_possible_values()
    # print (full_calc_possibles)
    # for ref,full in full_calc_possibles.items():
    #     if grid_possibles[ref]!=full:
    #         print (f"ref {ref}")



    # end of loop - but shouldn't ever get here as it's a while true

    return "something weird",iteration_cycles_counter










def real_iterate_multi(timeout=None,max_solutions=2, return_grids=False):
    #Iterating solver -- can find multiple solutions

    global iterate_number_count, iterate_cell_count, max_iters
    if timeout:
        timeout_time=time.time()+timeout
    #verbose=True #************
    grid_givens=grid.copy()
    # givens - the grid is a set of given numbers to keep and iterate around
    success = False
    total_solutions=0
    solution_grids_found=[]
    numbers_to_try_stack = {}
    cell_iter_no = 0
    keep_iterating = True
    timed_out = False
    next_step = "starting"
    while keep_iterating:
        # let's start loop off
        #print("next step",next_step)
        if next_step == "ascend":
            if cell_iter_no < num_rows * num_cols - 1:  # TODO create variable
                cell_iter_no += 1
                iterate_cell_count += 1
                # if verbose:
                #     if iterate_cell_count % 50000 == 0:
                #         elapsed = time.time() - start_time
                #         if not elapsed:
                #             rate = 0
                #         else:
                #             rate = iterate_cell_count / elapsed
                #         print("iterate counts", iterate_cell_count, iterate_number_count, "cell", cell_iter_no,
                #               "time", elapsed, "rate", rate)
            else:
                # got as far as end cell - complete
                total_solutions+=1
                # print(f"solution found --- number {total_solutions}  cell  number {cell_iter_no}")
                # print (grid)
                solution_grids_found.append(grid.copy())
                next_step="descend"
                if total_solutions>=max_solutions:
                    break

        if next_step == "descend":
            if grid_givens[rc]==0:
                grid[rc] = 0
            cell_iter_no -= 1
            if cell_iter_no < 0:
                next_step = "EXHAUSTED"
                break

        rc = row_col[cell_iter_no]
        #print ("rc",rc)

        if grid_givens[rc] and next_step=="starting":
            next_step="ascend"

        if grid_givens[rc]==0:
            #only do the iterate part if it's not a 'given' -- ie its blank

            if next_step == "ascend" or next_step == "starting":
                max_nums, shapes = iter_shapes[cell_iter_no]
                nums_avail = list(range(1, max_nums + 1))
                for shape in shapes:
                    this_num = grid[shape]
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
            else: #keep trying numbers in this cell
                num_to_try = nums_avail.pop(0)
                numbers_to_try_stack[cell_iter_no] = nums_avail

                grid[rc] = num_to_try
                iterate_number_count += 1
                # now let's check if valid
                valid = True
                neighbours = iter_nonshape_neighbours[cell_iter_no]
                for nb in neighbours:
                    if grid[nb] == num_to_try:
                        valid = False
                        break

                # if ok - ascend a level in iteration
                if valid:
                    if timeout:
                        ok_continue=(time.time()<timeout_time)
                    else:
                        ok_continue=(iterate_cell_count<max_iters)
                    timed_out=not ok_continue
                    if cell_iter_no < num_rows * num_cols - 1 and ok_continue:
                        iterate_cell_count += 1
                        next_step = "ascend"
                        # if iterate_cell_count % 10000 == 0:
                        #     elapsed = time.time() - start_time
                        #     if not elapsed:
                        #         rate = 0
                        #     else:
                        #         rate = iterate_cell_count / elapsed
                        #     print("iterate counts", iterate_cell_count, iterate_number_count, "time", elapsed,
                        #           "rate", rate)

                else:
                    # doesn't work try next number
                    next_step = "inc_number"
                    grid[rc] = 0

        else:
            pass
            #print(f"skipped {rc}")

        # this is end of while loop I think

    # print(grid)
    # END OF ITERATION

    if total_solutions==1:
        success=True

    if timed_out:
        total_solutions=-1

    if return_grids:   #return a second variable of the grids found?? default=No
        return total_solutions, solution_grids_found
    else:
        return total_solutions


def create_iterate_lookups():
    global iter_shapes, iter_nonshape_neighbours, row_col
    # to save time with a large recursive function, use some additional data lookups
    iter_shapes = {}  # not working yet!!
    iter_nonshape_neighbours = {}
    row_col = {}
    for i in range(num_cols * num_rows):
        r = i // num_cols
        c = i % num_cols
        row_col[i] = (r, c)
        shape_no = grid_shapes[r, c]
        shapes = shape_coords[shape_no]
        max_nums = len(shapes)
        iter_shapes[i] = (max_nums, shapes)
        neighbours = get_neighbours(r, c)
        for nb in neighbours:
            if nb in shapes:
                neighbours.remove(nb)
        iter_nonshape_neighbours[i] = neighbours


def puzzle_buildup(maxi_timeout=10):
    global grid

    # print("bottom up buildup")
    solution_grid = grid.copy()
    grid = np.zeros((num_rows, num_cols), dtype=int)
    starting_givens = max(num_rows,num_cols) # instead of 10 start with whichever is the biggest dimension
    max_cells = num_rows * num_cols - 1
    added = 0
    while added < starting_givens:
        cell_to_add = random.randint(0, max_cells)
        r = cell_to_add // num_cols
        c = cell_to_add % num_cols
        if grid[r, c] == 0:
            grid[r, c] = solution_grid[r, c]
            added += 1

    keep_going = True
    start_time=time.time()

    # now keep building up the grid one number at a time until uniquely solveable
    while keep_going:

        # now check whether this grid is uniquely solveable -- and return a  copy of the first 2 solutions
        grid_to_solve = grid.copy()  #keep a copy of just the puzzle start numbers as this will be overwritten
        result_successes, grids_found = real_iterate_multi(max_solutions=2, return_grids=True, timeout=maxi_timeout/3) #make sure mini timeout short enough to return here in time for maxi timeout
        # print("solutions: ", result_successes)
        grid = grid_to_solve
        if result_successes > 1:
            #more than one success - keep going with building up the puzzle
            #but first check for an overall timeout
            if time.time()>start_time+maxi_timeout:
                print ("no solution - global/maxi timeout  -- optimised solver should help stop that!")
                return None

            #print(grids_found)
            #print(np.array_equal(grids_found[0], grids_found[1]))
            # if more than one solution work out the 'difference' between them
            #NEW: check solution 1 against solution 0, not against the ideal 'solution_grid' -- shouldn't really matter now - a solution is a solution
            diff = (grids_found[1] - grids_found[0])  # subtract to find which elements are not same
            #print(diff)
            # print ("1",grids_found[1])
            # print("sol",grids_found[0])
            diff_loc = np.argwhere(diff)  # just give locations of elements that are non-zero (ie weren't same)
            # print(diff_loc)
            # now use one of locations to add the next number into the grid
            cell_to_add = (diff_loc[0, 0], diff_loc[0, 1])
            # print(cell_to_add)
            grid[cell_to_add] = grids_found[0][cell_to_add]
        elif result_successes==1:
            # print("success - unique solutions")
            #print(grids_found)
            # keep_going = False
            return grids_found[0]
        else:
            #in this case no solution found - must be because of timeout running  individual solver
            #TODO - change the multi solver to use the new optimised solver
            print ("no solution -- individual solver timeout")
            return None


if __name__ == '__main__':
    ##adding this so hopefully we can reuse procedures in other files

    import turtle

    #TODO eventually use AI to predict if a grid is solveable!!

    #global variables used by generator functions
    num_cols = 10   #9  # 8 or 13
    num_rows = 7   #7  # 6 or 10

    #settings
    #random.seed(1234566) #***FOR A BIT OF PREDICTABILITY
    eliminate_fatal_shapes = True
    verbose = False
    max_iters = 1e6 #1e8  # 1e99
    #timeout=4
    outer_loop = True
    stop_on_success = True #False #True #False
    grids_to_try = 5  # if not stop on success how long to continue

    via_api = False #True

    #variables
    success_count = 0
    timeouts_count = 0

    all_shape_count = {}
    success_shape_count = {}

    #global variables for display functions
    # SETUP
    cell_draw_size = 40
    horiz_offset = cell_draw_size / 2
    vert_offset = cell_draw_size * .9
    row_width = cell_draw_size * (num_cols - 1)
    display_build = False #True #False #False #True  # False #show shapes  building up slowly, or jump in one go
    start_time_all_grids = time.time()
    time_grid_gen=0
    time_grid_solve=0

    grids_tried = 0
    found_one_yet = False
    max_iters_used = 0
    fatal_eliminated = 0

    single_cell_success_tracker,single_cell_fail_tracker=[],[]

    screen = turtle.Screen()
    screen.delay(0)
    screen.tracer(0)
    screen.setup(startx=50,starty=50)  #where the turtle screen starts on the computer screen
    if display_build: screen.tracer(1)

    pen = turtle.Turtle()
    pen.speed(0)


    def draw_grid():
        global start_coords, r, c
        start_coords = (-screen.window_width() / 2 + cell_draw_size, screen.window_height() / 2 - cell_draw_size)
        row_width = cell_draw_size * (num_cols - 1)
        line_light = 1
        line_heavy = 3
        pen.up()
        # pen.setpos(-row_width, +row_width)
        pen.setpos(start_coords)
        pen.down()
        # print(grid.shape)
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
        pen.up()


    def fill_cell(coord, colour="orange"):
        c, r = coord
        pen.setpos(start_coords[0] + r * cell_draw_size, start_coords[1] - c * cell_draw_size)
        pen.fillcolor(colour)
        pen.setheading(0)  # east
        pen.begin_fill()
        for i in range(4):
            pen.forward(cell_draw_size)
            pen.right(90)
        pen.end_fill()



    # Keyboard Exception Handling -- idea = allow CTRL-C to exit long loop and still print results
    # actually doesn't quite work -- CtRL-C doesn't stop it now, but the stop button in PyCharm does
    try:

        # OUTER LOOP - generate a grid - run at least once
        while not found_one_yet:

            create_blank_grids()

            draw_grid()
            if display_build: screen.tracer(1)

            # reset grid background to white
            for r in range(num_rows):
                for c in range(num_cols):
                    fill_cell((r, c), "white")

            bad_shape1 = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 2]]  # C Shape
            bad_shape2 = [[0, 0], [0, 1], [0, 2], [1, 0], [2, 0]]  # Big Corner

            bad_shapes = translated_shapes(bad_shape1)
            bad_shapes = bad_shapes + translated_shapes(bad_shape2)
            # this is now a full list of all  permutations of bad shapes

            generator_type = "predetermined_list"  #"random_walk"  #"predetermined_list"  #"random_walk"  #

            if generator_type == "random_walk":

                ######START GENERATING RANDOM GRID HERE

                # start_point=(5,5)
                start_point = (int(num_rows / 2), int(num_cols / 2))

                this_point = start_point
                # moves=["up","down","left","right"]
                move_coord = [(-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)]
                # colours=["orange","blue","green","cyan","magenta","pink","red","olive","orchid","seagreen","yellow"]

                for shape_number in range(1, 90):
                    this_shape = []
                    length = 0
                    # colour=colours[shape_number%len(colours)]
                    colour = random_colour()
                    # colour=(random.randint(5,95),random.randint(5,95),random.randint(0,95))
                    keep_going = True
                    tries = 0
                    while keep_going:
                        choice = random.randint(0, 4)
                        move = move_coord[choice]
                        new_point = tuple(np.add(this_point, move))

                        # check valid
                        valid = True
                        if not (0 <= new_point[0] <= num_rows - 1): valid = False
                        if not (0 <= new_point[1] <= num_cols - 1): valid = False
                        if valid and grid_shapes[new_point] > 0: valid = False

                        # add a routine to check for fatal shape here
                        if eliminate_fatal_shapes and length == 4:
                            temp_shape = this_shape[:]  # create new copy of this_shape
                            temp_shape.append(new_point)
                            # now check if this shape is one of the fatal shapes
                            temp_shape.sort()
                            first_coord = temp_shape[0]
                            temp_shape_arr = np.array(temp_shape)
                            temp_shape_arr = temp_shape_arr - (first_coord)
                            temp_shape = temp_shape_arr.tolist()
                            # this is to rebase shape
                            # TODO - this code repeated a few times, make a function

                            if temp_shape in bad_shapes:
                                # the shape we are building is a fatal shape - stop here
                                # print ("fatal shape", temp_shape)
                                valid = False
                                fatal_eliminated += 1
                                # screen.tracer(1)
                                # for sh in  this_shape:
                                #     fill_cell(sh,"red")
                                # fill_cell(new_point,"red")
                                # screen.tracer(0)
                                # time.sleep(.5)

                        if valid:
                            this_point = new_point
                            if this_point not in this_shape:
                                this_shape.append(this_point)
                                fill_cell(this_point, colour)
                                length += 1
                            if length == 5: keep_going = False
                        else:
                            if length == 0 and tries > 999995:
                                this_point = new_point
                                print("stuck", this_point)

                        tries += 1
                        if tries > 35: keep_going = False

                    # print("shape: ",shape_number, "length: ",length, "tries: ",tries) #this_shape)

                    for cell in this_shape:
                        grid_shapes[cell] = shape_number
                    # print (grid_shapes)
                    #print()
                    if display_build:  time.sleep(.02)

                    if this_shape == []:
                        # print("bit stuck")
                        # bit stuck - find some blank space to go back to
                        empty_cell = []
                        for r in range(num_rows):
                            if empty_cell: break
                            for c in range(num_cols):
                                if grid_shapes[r, c] == 0:
                                    empty_cell = (r, c)
                                    # print("stuck outcome:",empty_cell)
                                    break
                        if empty_cell:
                            this_point = empty_cell
                        else:
                            # we've finished
                            if verbose: print("****finished?")
                            break
            # ***END OF RANDOM WALK GENERATE ROUTINE

            elif generator_type == "predetermined_list":
                gen_predet_shapes()


            else:  # simply give a shape

                grid_shapes = np.array([[6, 3, 3, 3, 3, 4],
                                        [6, 3, 2, 2, 2, 4],
                                        [6, 7, 2, 2, 1, 4],
                                        [6, 7, 7, 1, 1, 4],
                                        [6, 7, 7, 1, 1, 9]])

                grid_shapes2 = np.array([[3, 3, 3, 6, 6, 6],
                                         [3, 4, 2, 2, 2, 6],
                                         [3, 4, 4, 2, 2, 6],
                                         [4, 4, 10, 1, 1, 1],
                                         [8, 8, 8, 8, 1, 1]])

            if verbose: print(grid_shapes)
            draw_grid()

            shape_coords=get_shape_coords()

            #turtle.done()

            #single cell check
            single_cell_count=0
            for shape_no, shape in shape_coords.items():
                if len(shape)==1:
                    single_cell_count+=1
            print ("single cell: ",single_cell_count)
            #TODO Next -- maybe go through all shapes and see how many non-5 cell neighbours they have





            # keep count on which shapes are used - useful when looping multiple grids
            for shape_no, shape in shape_coords.items():
                # I intended to sort shape coords, but they start off in right order b/c of way generated
                first_coord = shape[0]
                rebased_shape = [(x[0] - first_coord[0], x[1] - first_coord[1]) for x in
                                 shape]  # my first list comprehension!!
                # rebased_shape_array = np.array(shape) - first_coord
                rebased_shape = tuple(rebased_shape)
                if rebased_shape in all_shape_count:
                    all_shape_count[rebased_shape] += 1
                else:
                    all_shape_count[rebased_shape] = 1


            def display_newnumber(num, rc_tuple, colour="blue"):
                xpos = start_coords[0] + cell_draw_size * rc_tuple[1] + horiz_offset
                ypos = start_coords[1] - cell_draw_size * rc_tuple[0] - vert_offset  # down is negative
                pen.setpos(xpos, ypos)
                pen.color(colour)
                pen.write(num, align="center", font=("Comic Sans MS", 18, "normal"))



            def recurse(cell_iter_no):
                global iterate_number_count, iterate_cell_count, max_iters
                success = False
                rc = row_col[cell_iter_no]
                # r=cell_iter_no//num_cols
                # c=cell_iter_no%num_cols

                max_nums, shapes = iter_shapes[cell_iter_no]
                # shape_no=grid_shapes[(r,c)]
                # shapes=shape_coords[shape_no]
                # max_nums=len(shapes)

                nums_avail = list(range(1, max_nums + 1))
                for shape in shapes:
                    this_num = grid[shape]
                    if this_num in nums_avail:
                        nums_avail.remove(this_num)

                for num_to_try in nums_avail:
                    grid[rc] = num_to_try
                    iterate_number_count += 1
                    # if iterate_number_count%500==0:
                    #    display_newnumber("@",(r,c),"white")
                    #    display_newnumber(num_to_try,(r,c))
                    # print ("#",cell_iter_no,"rc",r,c,"num",num_to_try)

                    # now let's check if valid
                    valid = True
                    # for shape in shapes:
                    #     if shape!=(r,c) and grid[shape]==num_to_try:
                    #         valid=False
                    neighbours = iter_nonshape_neighbours[cell_iter_no]
                    for nb in neighbours:
                        if grid[nb] == num_to_try:
                            valid = False
                            break

                    # if ok
                    if valid:
                        if cell_iter_no < num_rows * num_cols - 1 and iterate_cell_count < max_iters:
                            iterate_cell_count += 1

                            if verbose:
                                if iterate_cell_count % 10000 == 0:
                                    elapsed = time.time() - start_time

                                    if not elapsed:
                                        rate = 0
                                    else:
                                        rate = iterate_cell_count / elapsed
                                    print(f"iterate counts {iterate_cell_count:,}", '{:,}'.format(iterate_number_count),
                                          "time", elapsed, "rate", rate)
                                    # f"{num:,}"
                            result = recurse(cell_iter_no + 1)
                            if result:
                                success = True
                                break
                            else:

                                success = False  # keep trying numbers

                        else:
                            # we've actually completed
                            success = True

                            break

                    # otherwise go up a number in for loop
                    grid[rc] = 0
                    # display_newnumber(num_to_try, (r, c),"white")

                if not success:
                    # run out of numbers in this cell
                    grid[rc] = 0

                # print(grid)
                return (success)








            #Iteration Prep
            iterate_cell_count = 0
            iterate_number_count = 0
            start_time = time.time()


            create_iterate_lookups()

            if via_api:
                returned=helper_functions.solve_via_api(grid_shapes,max_iters=max_iters,url_override="local",timeout=timeout)
                timed_out=returned["timed_out"]
                success= returned["success"]
                grid=np.array(returned["grid_values"])
            else:

                # success,timed_out = real_iterate()
                success, timed_out = real_iterate()
                #TODO - need to change function so it clearly returns how many solutions or at least whether 1 or more
                #TODO first time you run it, only need it to be at least 1, then set that solution as the base
                #TODO then next up you need to run the solver, knowing what the givens are -- don't think I've got that yet

            #print ("WAS IT A SUCCESS?",success)


            if timed_out:
                timeouts_count += 1
            else:
                print ("result achieved -- success?", success)

            # if iterate_cell_count > max_iters_used:
            #     max_iters_used = iterate_cell_count




            if success:
                success_count += 1
                single_cell_success_tracker.append(single_cell_count)


                print(grid)
                print(grid_shapes)

                # keep count on which shapes are used - SUCCESS VERSION -  useful when looping multiple grids
                for shape_no, shape in shape_coords.items():
                    # I intended to sort shape coords, but they start off in right order b/c of way generated
                    first_coord = shape[0]
                    rebased_shape = [(x[0] - first_coord[0], x[1] - first_coord[1]) for x in
                                     shape]  # my first list comprehension!!
                    # rebased_shape_array = np.array(shape) - first_coord
                    rebased_shape = tuple(rebased_shape)
                    if rebased_shape in success_shape_count:
                        success_shape_count[rebased_shape] += 1
                    else:
                        success_shape_count[rebased_shape] = 1


                def remove_numbers(grid,number_to_remove=1):
                    max_cells=num_rows*num_cols-1

                    removed=0
                    while removed<number_to_remove:
                        start_point = random.randint(0, max_cells)
                        start_point+=1
                        if start_point>max_cells:
                            start_point=0
                        r=start_point//num_cols
                        c=start_point%num_cols
                        if grid[r,c]:
                            grid[r,c]=0
                            removed+=1
                    return grid



                ##################################
                ##now let's try to come up with single answer?
                puzzle_set="buildup"

                #this next bit redundant - superseded by "buildup" method -- TODO: delete and check still works?
                # if puzzle_set=="reduce":
                #     print ("******PRUNING!....")
                #     #let's remove numbers on a loop until we no longer get a single solution#
                #     keep_removing=True
                #     grid = remove_numbers(grid, 8)
                #     while keep_removing:
                #         last_known_unique_soln=grid.copy()
                #         grid=remove_numbers(grid,3)
                #         print ("Removed 3**")
                #         print(grid)
                #         result_successes = real_iterate_multi()
                #
                #         # TODO probably what I need to do here is:
                #         # more sophisticated way of removing numbers
                #         # make sure to remove evenly across the shapes so you don't end up with some empty and some stacked
                #         #or even, once you've found a full solution, reset back to empty grid and slowly fill it with numbers from the real solution (shape by shape) until it is uniquely solveable
                #
                #
                #
                #         print(grid)
                #         if result_successes>1:
                #             break
                #     print ("**stop")
                #     print (last_known_unique_soln)

                if puzzle_set=="buildup":
                    puzzle_buildup()



                display_numbers()
                turtle.done()
















            else:
                single_cell_fail_tracker.append(single_cell_count)

            elapsed = time.time() - start_time
            time_grid_solve += elapsed

            if elapsed > 0:
                end_rate = iterate_cell_count / elapsed
            else:
                end_rate = 0

            grids_tried += 1

            if True:  # verbose:
                print(f"tries: {grids_tried}  iterate counts", iterate_cell_count, iterate_number_count, "time", elapsed,
                      "rate", end_rate)


            # now numbers



            zero_override = "X" if not success and not timed_out  else None
            display_numbers(zero_override=zero_override)

            if success or grids_tried > 0:
                found_one_yet = success  # True to stop

            if not stop_on_success:
                found_one_yet = (grids_tried >= grids_to_try)

            if not (outer_loop): found_one_yet = True  # stop if not meant to be outer looping

    except KeyboardInterrupt:
        print("************KEYBOARD INTERRUPT!!************")
        # but still carry on

    ################################################
    ###### LOOP HAS FINISHED -- NOW ANALYSE RESULTS
    print("**FINISHED** total grids tried", grids_tried,
          f"successes: {success_count}  timeouts:{timeouts_count}   fatal shapes blocked:{fatal_eliminated}")

    print("******SHAPES*****")


    names = []
    shapes = []
    for count, val in enumerate(standard_shapes_long_as_list):
        if count % 2 == 0:
            names.append(val)
        else:
            shapes.append(val)

    all_tot = 0
    success_tot = 0
    for sh in all_shape_count:
        # print (all_shape_count[sh],success_shape_count.get(sh),sh)
        all_tot += 0 if all_shape_count[sh] is None else all_shape_count[sh]
        success_tot += 0 if success_shape_count.get(sh) is None else success_shape_count[sh]

    print("total different shapes:", len(all_shape_count))
    print("total all  shapes", all_tot, "total success", success_tot)

    print("*****THAT WAS RAW SCORES***** ")
    print("****NOW FOR COLLATING.....****")
    collated_list = {}
    for sh in all_shape_count:
        shape_permutations = translated_shapes(sh)
        lowest_perm = shape_permutations.copy()
        lowest_perm.sort()
        lowest_perm = lowest_perm[0]

        lowest_perm_string = str(lowest_perm)
        if lowest_perm_string in collated_list:
            orig_score = collated_list[lowest_perm_string]
            new_score_0 = orig_score[0] + all_shape_count[sh]

            orig_score_1 = 0 if orig_score[1] is None else orig_score[1]
            # if not orig_score_1: orig_score_1=0
            new_score_1 = 0 if success_shape_count.get(sh) is None else success_shape_count[sh]
            # if not new_score_1: new_score_1=0
            new_score_1 = orig_score_1 + new_score_1
            if new_score_1 == 0: new_score_1 = None
            new_score = (new_score_0, new_score_1)

            # score_here=(score_here[0]+all_shape_count[sh],score_here[1]+success_shape_count.get(sh))
        else:
            new_score = (all_shape_count[sh], success_shape_count.get(sh))
        collated_list[lowest_perm_string] = new_score

    # print(collated_list)

    any_new_shapes = False
    all_tot = 0
    success_tot = 0
    for sh in collated_list:
        # print (collated_list[sh],sh)
        all_tot += collated_list[sh][0]
        success_tot += 0 if collated_list[sh][1] is None else collated_list[sh][1]
        sh_list_form = eval(sh)  # convert back from string to a list
        if sh_list_form not in standard_shapes_long_as_list:
            print("**********NEW SHAPE FOUND!!!**********")
            print(sh)
            any_new_shapes = True
            # I don't  expect this to happen!

    print("length: ", len(collated_list))
    print("total all  shapes", all_tot, "total success", success_tot)

    # check all shapes found appear in standard shapes list


    # create a dataframe of collated list
    # loop through standard shapes, create a column for name, shape, total , success, success %

    all_tot = 0
    success_tot = 0
    tot_per_shape = []
    success_per_shape = []
    success_rate_per_shape = []
    count = 0
    for shape in shapes:
        # print (count,tot_per_shape)
        count += 1
        shape_str = str(shape)
        scores = collated_list.get(shape_str)
        if scores:
            tot_per_shape.append(scores[0])

            if scores[1]:
                success_per_shape.append(scores[1])
                success_rate_per_shape.append(round(scores[1] / scores[0] * 100))
            else:
                success_per_shape.append(0)
                success_rate_per_shape.append(None)
        else:
            tot_per_shape.append(0)
            success_per_shape.append(0)
            success_rate_per_shape.append(0)

    print(tot_per_shape)
    print(success_per_shape)
    print(success_rate_per_shape)

    print("******")
    dfdata = {"name": names, "shape": shapes, "total": tot_per_shape, "success": success_per_shape,
              "success_rate": success_rate_per_shape}

    pd.set_option('display.max_columns', None)
    df = pd.DataFrame(dfdata)
    df.insert(2, 'length', df["shape"].str.len())
    #df["length"]=df["shape"].str.len()
    print(df.drop(columns=["shape"]))

    fails=grids_tried-success_count-timeouts_count

    print("**FINISHED** SUMMARY***")
    print(f"grid size = {num_rows},{num_cols}")
    print("total grids tried", grids_tried,
          f"successes: {success_count}  fails: {fails} timeouts:{timeouts_count}   fatal shapes blocked:{fatal_eliminated}")
    #print("Python impl: ", platform.python_implementation())

    full_elapsed = round(time.time() - start_time_all_grids, 1)
    if full_elapsed > 0:
        end_rate = round(full_elapsed / grids_tried, 2)
    else:
        end_rate = 0
    print(f"Total time taken {full_elapsed}    Time per grid  {end_rate}")
    time_grid_gen=full_elapsed-time_grid_solve
    gen_rate=time_grid_gen / grids_tried
    print(f"total grid gen {time_grid_gen}  and rate {gen_rate}")

    # a duplicate
    if any_new_shapes:
        print("*****NEW SHAPE FOUND&********")
    else:
        print("(no new shapes)")

    scsucess_av=0 if len(single_cell_success_tracker)==0 else sum(single_cell_success_tracker)/len(single_cell_success_tracker)
    scfail_av = 0 if len(single_cell_fail_tracker) == 0 else sum(single_cell_fail_tracker) / len(single_cell_fail_tracker)
    print ("single cells...")
    print ("success:  ",scsucess_av,single_cell_success_tracker)
    print ("fail: ",scfail_av,single_cell_fail_tracker)




    turtle.done()
