#Puzzle
#This file aiming to refactor suguru into a tidier, class based approach
import copy
import random, time, json
import sys
from pprint import pprint
from collections import defaultdict, deque

class Puzzle:


    def __init__(self,rows,cols):
        #set dimensions of puzzle
        self.rows=rows
        self.cols=cols

        self.iterate_part_timer=0
        self.iteration_counter=0
        self.iteration_timeout_limit=1 #seconds

        #now create two blank (filled with zero) grids:
        #self.values= [[0 for c in range (cols)] for r in range(rows)]   #values ie only 1-5 possible, in each cell
        self.solution= [[0 for c in range (cols)] for r in range(rows)]   #values ie only 1-5 possible, in each cell
        self.shapes= [[0 for c in range (cols)] for r in range(rows)]   #shape number that cell belongs to - defines shapes within the grid
        self.givens = [[0 for c in range(cols)] for r in range(rows)]  # values ie only 1-5 possible, in each cell

        #load the lookup table of all possible shapes and their permutations
        #this has been previously generated from trial and error - and then doing a rotation of each etc - see gridgenerate create shape permutations and translate shapes
        #should stay a constant throughout
        self.ALL_SHAPE_PERMUTATIONS=self.load_all_shape_permutations()

    def load_all_shape_permutations(self):
        #original shapes come from gridgenerate.py - create_shape_permutations_and_save_to_file()
        with open("shape_permutations.json", 'r') as f:
            tempdict = json.load(f)
        return tempdict

    def clear_solution(self):
        self.solution = [[0 for c in range(self.cols)] for r in range(self.rows)]  # values ie only 1-5 possible, in each cell



    def in_bounds(self,coord):
        valid = (0 <= coord[0] <= self.rows - 1) and (0 <= coord[1] <= self.cols - 1)
        return valid

    def get_solution(self,coord):
        return self.solution[coord[0]][coord[1]]

    def get_shape(self,coord):
        return self.shapes[coord[0]][coord[1]]

    def set_solution(self,coord,value):
        self.solution[coord[0]][coord[1]]=value

    def set_shape(self,coord,value):
        self.shapes[coord[0]][coord[1]]=value

    def dump_solution(self):
        print("SOLUTION")
        for row in self.solution:
            print(row)

    def dump_shapes(self):
        print("SHAPES")
        for row in self.shapes:
            print(row)

    def dump_both(self):
        for r in range(self.rows):
            poss = []
            for c in range (self.cols):
                if self.solution[r][c]==0:
                    poss.append(len(self.cell_possibles[r,c]))
                else:
                    poss.append(0)

            shapes=self.shapes[r]
            shapes_as_letters=[(chr(ord('@')+number)) for number in shapes]

            #print(self.shapes[r],"   ",self.solution[r]," ... ",poss)
            print(shapes_as_letters,"   ",self.solution[r]," ... ",poss)
            #print( self.solution[r], " ... ", poss)
        print()


    def next_free_space_spiral(self,start_coord):
        # this function spirals outwards from starting coord (r,c) until it finds an empty cell
        # empty meaning -  the shapes result for that cell is zero

        if self.get_shape(start_coord) == 0:
            return start_coord
            # if starting point already is blank

        move_coord_4 = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        #TODO: Add Anti clockwise, and random start

        new_point = start_coord
        step_size = 0

        for i in range(max(self.cols, self.rows)):
            any_in_bounds = False
            for move in move_coord_4:
                if move[0] == 0:
                    step_size += 1  # increase step size every other step, that seems to make a spiral
                for steps in range(step_size):

                    new_point = add_coords(new_point, move)
                    if self.in_bounds(new_point):
                        any_in_bounds = True
                        if self.get_shape(new_point) == 0:
                            return new_point

            if not any_in_bounds:
                return None  # spiral reached outside so stop

    def colour_shapes(self):
        shape_colours = {}
        shape_cells = {}

        # Group cells by shape
        for r in range(self.rows):
            for c in range(self.cols):
                shape = self.shapes[r][c]
                if shape not in shape_cells:
                    shape_cells[shape] = []
                shape_cells[shape].append((r, c))

        def get_adjacent_shapes(shape):
            adjacent = set()
            for r, c in shape_cells[shape]:
                for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.rows and 0 <= nc < self.cols and self.shapes[nr][nc] != shape:
                        adjacent.add(self.shapes[nr][nc])
            return adjacent



        # Color shapes
        for shape in shape_cells:
            adjacent_shapes = get_adjacent_shapes(shape)
            adjacent_colors = {shape_colours[adj] for adj in adjacent_shapes if adj in shape_colours}
            for color in range(1, 7):  # We only need to check up to 4 colors #yeah, but it's a bit boring!!
                if color not in adjacent_colors:
                    shape_colours[shape] = color
                    break


        self.shape_colours=shape_colours
        return shape_colours


    def generate_grid_shapes(self,single_cell_stop=True):
        #function to generate a full grid of shapes - based on pre-loaded shapes (and permutations)

        def get_adjacent_cells(cell_coords):
            adjacent = set()
            r,c=cell_coords
            for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    adjacent.add((nr,nc))
            return adjacent

        # random choice of start -  biased to middle third
        start_point = (
            random.randint(self.rows // 3 - 1, self.rows * 2 // 3 - 1),
            random.randint(self.cols // 3 - 1, self.cols * 2 // 3 - 1) )

        #shuffle at start would go here if wanted -- or some other shuffle later

        go = 0
        shape_number = 1
        single_cell_count = 0
        verbose=False
        active_point=start_point


        #LOGIC SHOULD BE:
        #pick a start point
        #Run a loop
        #in this place, go through each shape, each permutation, each starting position -- will it fit
        #make sure it doesn't leave an awkward gap
        #if it fits, save the shape number in every cell -- move on with the loop -- move to next point, using spiral
        #(if it doesn't keep trying)
        #if you run out of options, start all over again

        #print("All Shapes - length",len(self.ALL_SHAPE_PERMUTATIONS),self.ALL_SHAPE_PERMUTATIONS)

        shapes_as_dict={s[0]:s[1] for s in self.ALL_SHAPE_PERMUTATIONS}
        #print(shapes_as_dict.keys())
        #print("ASD",shapes_as_dict)

        shape_pref_order=['snail','steps','gun','L','line-5','seahorse', 'cross', 'T', 'snake', 'S'] #from an experiment

        working_shape_list_longer=[]
        for shape_name in shape_pref_order:
            working_shape_list_longer.append([shape_name,shapes_as_dict[shape_name]])

        working_shape_list_top=working_shape_list_longer[0:6]
        working_shape_list_mid = working_shape_list_longer[6:]
        working_shape_list_top_original=copy.deepcopy(working_shape_list_top)



        #originally longer is 0to14-so say 0:15 // shorter 15,  then 12>>
        #working_shape_list_longer=copy.deepcopy(self.ALL_SHAPE_PERMUTATIONS[0:12])
        working_shape_list_shorter=copy.deepcopy(self.ALL_SHAPE_PERMUTATIONS[10:])

        # test=self.ALL_SHAPE_PERMUTATIONS[self.ALL_SHAPE_PERMUTATIONS.index("snail")]
        # print("TT",test)



        keep_going=True
        #MAIN SHAPE LOOP
        while keep_going:

            if verbose:
                print(f"Goes {go} Active Point",active_point)
                self.dump_shapes()

            if go%2==0:
                random.shuffle(working_shape_list_top)
                # top_one=working_shape_list_top[:1]
                # working_shape_list_top=working_shape_list_top[1:]+top_one
                #print(working_shape_list_top)
                random.shuffle(working_shape_list_mid)

                if go%6==99:
                    working_shape_list_top=copy.deepcopy(working_shape_list_top_original)

            front_load=[]
            if go==0:
                front_load.append(random.choice(working_shape_list_shorter))
            working_full_shape_list = front_load + working_shape_list_top + working_shape_list_mid + working_shape_list_shorter
            #print(working_full_shape_list)
            # working_full_shape_list=front_load
            # working_full_shape_list.extend(working_shape_list_longer)
            # working_full_shape_list.extend(working_shape_list_shorter)

            #pprint(working_full_shape_list)



            for shape_name, shape_permutations in working_full_shape_list:
                if verbose: print("*****SHAPE:", shape_name)

                random.shuffle(shape_permutations)
                # shuffle permutations so the shapes don't tend to completely align automatically

                for shape_to_try in shape_permutations:
                    if verbose: print(shape_to_try)

                    for home_coord in shape_to_try:
                        # now alter which cell of the shape is the one to line up  on the starting cell
                        home_coord_offset = (-home_coord[0], -home_coord[1])
                        if verbose: print("home coord offset =", home_coord_offset)

                        # now check if it fits -- is each cell within bounds and empty
                        #assume valid until it proves otherwise
                        valid = True
                        for coord in shape_to_try:
                            adjusted_coord = add_coords(coord, active_point, home_coord_offset)
                            if verbose: print(adjusted_coord)
                            if not self.in_bounds(adjusted_coord) or self.get_shape(adjusted_coord)!=0:
                                valid = False
                                break

                                # last test - does it create a blocked off single cell (this is generally a bad thing)
                                # what's the logic for this?
                                # for every cell in the new shape, work out what are the "affected cells" - ie those that are directly adjacent (not diagonal)
                                # then for every affected cell, see if it is blank and see if its own direct sideways neighbours are completely blocked by existing or this new shape
                                # ideally if already blocked, then this is already a problem - leave it be
                                # so long as at least one sideways escape route, that's ok
                                # otherwise fail this shape


                            #single cell stop stuff - can add in later    
                            if single_cell_stop:
                                    if valid:
                                        # first establish affected cells
                                        affected_cells = set()
                                        shape_try_adjusted = []

                                        for coord in shape_to_try:
                                            # recalculate what the actual coordinates of the candidate shape are (we did this earlier, but probably not worth saving?)
                                            #first what is individual coordinate - need to use that for affected cells
                                            adjusted_coord = add_coords(coord, active_point, home_coord_offset)
                                            # then see which cells are affected (adjacent) to each of those
                                            affected_cells.update(get_adjacent_cells(adjusted_coord))  #which cells are sideways neighbours but within bounds
                                            #also keep tabs of whole shape - as cells that are already in the shape don't class as 'affected'
                                            shape_try_adjusted.append(adjusted_coord)

                                            #TODO: QUESTION SHOULD THIS BE ADD NOT UPDATE?
    
                                        for coord in affected_cells:
                                            if coord not in shape_try_adjusted and self.get_shape(coord) == 0:  # don't check members of prospective shape itself and affected cell needs to be empty not part of existing shape
                                                #now for every affected cell -- check all of their surrounding cells to see if blocked off
                                                sideways_neighbours = get_adjacent_cells(coord)
                                                empty_before_shape = 0
                                                empty_after_shape = 0
                                                # logic that follows - we need affected shapes to have at least 1 blank - after the shape has gone in (if had 0 before that's ok)
                                                for nb in sideways_neighbours:
                                                    if self.get_shape(nb) == 0:
                                                        empty_before_shape += 1
                                                        if nb not in shape_try_adjusted:
                                                            empty_after_shape += 1
                                                if empty_after_shape == 0 and empty_before_shape != 0:
                                                    single_cell_count += 1
                                                    if single_cell_count > 2:  # allow *some*
                                                        # TODO check how close?
                                                        # TODO Maybe check if this single cell shares a neighbouring shape with the others?
                                                        valid = False
                                                        # print (f"**single cell**  affected cell {coord} -- emptybefore  {empty_before_shape}  emptyafter {empty_after_shape}")
                                                        break
    
                                        # print (f"shape number {shape_number}-- valid {valid} -- shape coords {shape_try_adjusted} ** affected cells: {affected_cells}")


                        if valid: break
                    if valid: break
                if valid: break


            #print ("valid?", valid)

            if valid:
                for coord in shape_to_try:
                    adjusted_coord = add_coords(coord, active_point, home_coord_offset)
                    self.set_shape(adjusted_coord,shape_number)
            #self.dump_shapes()
            #now move on to next space - use spiral

            spiral_point=self.next_free_space_spiral(active_point)
            if not spiral_point:
                #nowhere else to go - in theory should be complete
                if any(0 in row for row in self.shapes):
                    print ("STUCK")
                    raise ValueError(f"SUGURU -- out of bounds but still have an unfilled shape?!")
                keep_going=False  #stop the loop
            else:
                active_point = spiral_point
                go+=1
                shape_number+=1

    def generate_shape_cells(self):
        #create lookup: #dictionary of all shapes and cells in those shapes
        self.shape_cells=defaultdict(list) #special type of dictionary that creates a list by default if key doesn't exist
        for r in range(self.rows):
            for c in range (self.cols):
                self.shape_cells[self.shapes[r][c]].append((r,c))

    def generate_linked_cells(self):
        #this is an extended list - of all cells in the same shape and all other neighbours (incl diagonal) - for every cell
        self.linked_cells=defaultdict(list)
        move_directions=[(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
        for r in range(self.rows):
            for c in range (self.cols):
                this_shape=self.shapes[r][c]
                cells_so_far=self.shape_cells[this_shape].copy()  #pull all cells in that shape
                cells_so_far.remove((r,c))  #but now remove this cell, only want surrounding ones
                for move_r,move_c in move_directions:
                    new_r,new_c = r+move_r, c+move_c
                    if 0<=new_r<self.rows and 0<=new_c<self.cols:
                        if (new_r, new_c) not in cells_so_far:
                            cells_so_far.append((new_r,new_c))
                self.linked_cells[(r,c)]=cells_so_far

    def initialise_cell_possibles(self,full_check=False):
        #generate dict of all possible values at each shape [aka "the domain"]
        self.cell_possibles={}
        for r in range(self.rows):
            for c in range (self.cols):
                self.cell_possibles[(r,c)]=set(range(1,len(self.shape_cells[self.shapes[r][c]])+1))
                #work out possibles by seeing how many cells in the r,c shape - generate a list starting with 1 up to that number and store in dictionary at r,c

        if full_check:
            #expect to use this when a partial solution in place - modify possibles accordingly
            for r in range(self.rows):
                for c in range(self.cols):
                    #print(r,c)
                    if self.solution[r][c]!=0:
                        #only bother with non-zero values
                        num=self.solution[r][c]
                        for linked in self.linked_cells[(r,c)]:
                            if num in self.cell_possibles[linked]:
                                self.cell_possibles[linked].remove(num)



    def pick_next_empty_cell(self,previous=False,use_lonely=False):
        """
        Picks the next empty cell to fill, prioritizing the cell with the fewest possible values.

        Args:
        - previous: The previously filled cell.
        - use_lonely: Whether to use the 'lonely' heuristic for cells with a single remaining possibility.

        Returns:
        A tuple containing the coordinates of the next cell and the forced number if applicable.
        """

        #function to find the next cell to iterate - which cell is empty and has fewest possible values
        #using Claude's list comprehension - hopefully is efficient
        starting_time_here=time.time()
        #return min((cell for cell in self.cell_possibles if self.solution[cell[0]][cell[1]] == 0), key=lambda cell: len(self.cell_possibles[cell]),default=False)
        next_cell= min((cell for cell in self.cell_possibles if self.solution[cell[0]][cell[1]] == 0), key=lambda cell: len(self.cell_possibles[cell]),default=False)
        self.iterate_part_timer+=(time.time()-starting_time_here)

        force_number=False

        if not next_cell:
            return False, False


        #note: adding this lonely cell checker does seem to cut the time down - by maybe half
        #TODO think if there is any more efficient way of running it

        if use_lonely and previous:
            #print("previous",previous)
            if len(self.cell_possibles[next_cell])>1:
                lonely_cell,number= self.lonely_numbers_check_all_linked(previous)
                if lonely_cell:
                    next_cell=lonely_cell
                    force_number=number
                    #print("LONELY - ",lonely,force_number)

        return next_cell, force_number

    def pick_next_empty_cell_GPT(self, previous=False, use_lonely=False):
        #ChatGPT version with improvements - allegedly!
        def cell_constraint_level(cell):
            # Number of linked cells that have fewer possibilities
            return sum(1 for linked in self.linked_cells[cell] if len(self.cell_possibles[linked]) < 2)

        starting_time_here = time.time()
        # Use both the number of possibles and the constraint level as heuristic
        next_cell=min(
            (cell for cell in self.cell_possibles if self.solution[cell[0]][cell[1]] == 0),
            key=lambda cell: (len(self.cell_possibles[cell]), cell_constraint_level(cell)),
            default=False
        )
        force_number = False

        if not next_cell:
            return False, False

        # note: adding this lonely cell checker does seem to cut the time down - by maybe half
        # TODO think if there is any more efficient way of running it

        if use_lonely and previous:
            # print("previous",previous)
            if len(self.cell_possibles[next_cell]) > 1:
                lonely_cell, number = self.lonely_numbers_check_all_linked(previous)
                if lonely_cell:
                    next_cell = lonely_cell
                    force_number = number
                    # print("LONELY - ",lonely,force_number)

        return next_cell, force_number


    def generate_iteration_lookups(self):
        #create all lookups needed to run iteration -- order is important as later ones depend on first
        self.generate_shape_cells()
        self.generate_linked_cells()
        self.initialise_cell_possibles()


    def better_solver(self, multi=False, use_lonely=True):
        #multi=flag whether to look for multiple solutions
        #use_lonely = flag whether to try to look ahead for search options where one number only possible in one place in a shape
        #TODO: add a unique check parameter
        # THIS VERSION TRIES TO FIND MULTIPLE SOLUTIONS
        # or more specifically check if solution is unique
        self.iteration_counter=0
        self.iteration_solutions_found=0
        self.iteration_start_Time=time.time()
        self.iteration_timeout = False
        return self._better_solve_recursion(multi=multi, use_lonely=use_lonely)


        #first, need to set up some useful variables to speed things up -- (quick lookup)
        #these done elsewhere:
        #-dictionary of all shapes and cells in those shapes -done
        #-dict of every cell and what the neighbours are for those cells (quick lookup) - done
        #-next we need to work out what values are possible in every cell [apparently aka domain in constraint lingo]
        #to start with this is just how many spaces in that shapes - later we will start eliminating based on solution values
        #DONE

        #now let's start thinking about our iterative, recursive / trackback (whch ?!?) approach

        #let's work out which cell to work on
        #first off call a function that finds the next empty cell that has the fewest possible values


    def _better_solve_recursion(self, next=False, previous=False, multi=False, use_lonely=False):
        #THIS VERSION TRIES TO FIND MULTIPLE SOLUTIONS
        #or more specifically check if solution is unique

        if time.time()-self.iteration_start_Time>self.iteration_timeout_limit:
            self.iteration_timeout=True
            return False


        if next:  #if the next cell has already been given as a parameter
            live_cell=next
        else:
            live_cell,force_number = self.pick_next_empty_cell_GPT(previous=previous,use_lonely=use_lonely)
            #print(f"Next= {live_cell}, force number {force_number}")


        if not live_cell:  #if there is no live cell returned, that's because we've done them all

            if not multi:
                return True

            else:

                #NEW BIT -- UNIQUENESS TESTER, DON'T JUST SIMPLY RETURN
                self.iteration_solutions_found += 1

                if self.iteration_solutions_found==1:
                    # print ("First Solution Found")
                    # self.dump_solution()
                    print("solution VALID?", self.is_whole_thing_valid())
                    self.first_trial_solution=copy.deepcopy(self.solution)
                    #now return False so we keep going with the search
                    return False
                else:
                    # print ("Second solution found")
                    # self.dump_solution()
                    #we can stop here, so return True (we don't want more than one)
                    return True

        self.iteration_counter+=1

        #now start to loop  through all possible values for that cell

        if force_number:
            numbers_to_try=[force_number]

        else:
            numbers_to_try=self.cell_possibles[live_cell]


        for num in numbers_to_try:
            #set the value
            self.set_solution(live_cell,num)
            #self.dump_both()


            #FORWARD LOOK / IMPACT CHECKER
            #now let's see what impact that has, now we've added another number
            #pull list of impacted cells - same shape + neighbours
            changes_made=[]
            broken_it=False

            for linked in self.linked_cells[live_cell]:
                #self.lonely_numbers_check_shape(self.get_shape(linked))  #TODO - remove
                #go through them all - if any are same value, remove that value, but note which cell we're removing from
                if num in self.cell_possibles[linked]:
                    if self.get_solution(linked)==0:  #only remove possibles from blank cells (not solved ones, which will have 1 residual possible)
                        self.cell_possibles[linked].remove(num)
                        #if len(self.cell_possibles[linked])==1:
                        #    single_location=linked
                        #tried this to speed up, but actually slightly slowed down by checking this too often
                        changes_made.append((linked,num))
                        if not self.cell_possibles[linked]:
                            broken_it=True
                            break
                            #if we've got no possible left, that's wrong, stop this process


            if not broken_it:
                #work out which shape the live cell is in and send
                broken_it,more_changes=self.surround_check_one_shape(self.shape_cells[self.get_shape(live_cell)], iterating=True)
                changes_made.extend(more_changes)


            ##TEMP
            #further quick check to see if anything now only has 1 possible
            '''
            for linked in self.linked_cells[live_cell]:
                if len(self.cell_possibles[linked])==1 and self.get_solution(linked)==0:
                    print (f"**SINGLE - live cell {live_cell}")
                    self.dump_both()
            '''



            #if any of the cells now have zero possibilities - this is a bad solution -- undo all changes made so far
            #otherwise carry on with the next number in the loop

            if not broken_it:
                success= self._better_solve_recursion(previous=live_cell, multi=multi,
                                                      use_lonely=use_lonely)  #send on current live cell to help with finding next cell to work on
                if success:
                    return True   #finish off neatly, returning from function if successful

            #if you get here, then something has gone wrong in iteration - reverse the changes
            self.set_solution(live_cell,0)
            for change in changes_made:
                self.cell_possibles[change[0]].add(change[1])

        #print ("DOWN")
        #self.dump_both()
        return False


            #if we've run out of numbers -- then exit the function with a bad result

            #[space here to optimise further by looking for any more cells that only have a single option after a new number added]

            #having updated the possibilities -- now call the recursive function again
            #recursive function needs to check if there are any empty cells left -- if not, hurray we're done -- return a positive message (this should propogate all the way back)


    def quick_original_solution_check(self,cell):
        if self.solution[cell[0]][cell[1]]!=self.original_solution[cell[0]][cell[1]]:
            self.dump_both()
            raise Exception ("New solution and original don't match - cell",cell)
        else:
            return True


    def logic_only_solver(self):
        #try to solve the puzzle using only logic - ie no brute force guessing
        #first reset cell possibles which we'll need a lot
        self.initialise_cell_possibles(full_check=True)
        #now see if we can solve, just using possibles removal




        self.dump_both()
        keepgoing=True
        loop=0
        while keepgoing:
            num=-1  #try to stop removing numbers we shouldn't
            loop+=1
            print("loop",loop)
            made_changes = False

            # let's check for a mistake
            gone_wrong=False
            for r in range(self.rows):
                for c in range(self.cols):
                    if self.solution[r][c]==0 and (self.original_solution[r][c] not in self.cell_possibles[(r,c)]):
                        print (f"*WENT WRONG AT {r,c} -- {self.original_solution[r][c]} is not in {self.cell_possibles[(r,c)]}" )
                        gone_wrong=True
            if gone_wrong:
                self.dump_both()
                raise Exception("possibles wrong")
            else:
                print(".")


            #find next cell with only 1 possible
            next_cell = min((cell for cell in self.cell_possibles if self.solution[cell[0]][cell[1]] == 0),
                            key=lambda cell: len(self.cell_possibles[cell]), default=False)
            if not next_cell:
                #we've solved it
                print ("hurray")
                return True
            possibles_here=self.cell_possibles[next_cell]
            if len(possibles_here)==0:
                print("**PROBLEM**")
            if len(possibles_here)==1:
                #only one option - good - we can update it
                num=possibles_here.pop()
                self.set_solution(next_cell,num)
                self.quick_original_solution_check(next_cell)
                print(f"filled {next_cell} with {num}")
                made_changes=True
            else:
                #run out of ones we can do with basic solver
                print("still in loop but can't do basic")

                self.dump_both()

                #try lonely solver
                for shape in self.shape_cells:
                    print("lonely solver - shape",shape)
                    result=self.lonely_numbers_check_shape(shape)
                    if result: break

                if result:
                    lonely_cell,num=result
                    print("lonely possibles",self.cell_possibles)
                    self.set_solution(lonely_cell, num)
                    self.quick_original_solution_check(lonely_cell)
                    next_cell=lonely_cell #to do follow_up
                    print(f"filled Lonely Cells {lonely_cell} with {num}")
                    made_changes = True

                else:  #lonely solver didn't help


                    #try surround check
                    removed=self.smaller_surrounded_check_all()
                    if removed:
                        print("surround smaller check has done something useful",removed)
                        made_changes=True

                    else:
                        #NEED LARGER SOLVER NOW

                        all_removed=[]
                        for shape in self.shape_cells.values():
                                print("UGH shape possibles at 1,5 --",self.cell_possibles[(1,5)])
                                broken_it, removed_list = self.surround_check_one_shape(shape,iterating=True,dumps=True) #need iterating flag
                                print(f"larger surround solver -- shape {shape} broken? {broken_it} removed {removed_list}")
                                if removed_list:
                                    print("surround LARGER check has done something useful")
                                    all_removed.append(removed_list)
                                    made_changes = True
                                    self.dump_both()

            if not made_changes:
                keepgoing=False




            #TODO - move this or only run when we've actually made changes
            #now update possibles based on the change - just check  'linked_cells'
            for linked in self.linked_cells[next_cell]:
                if num in self.cell_possibles[linked]:
                    if self.get_solution(linked)==0:  #only remove possibles from blank cells (not solved ones, which will have 1 residual possible)
                        self.cell_possibles[linked].remove(num)


        print("STEP 1 - REMOVING POSSIBLES - RUN OUT ")

        self.dump_both()
        print("LONELY NUMBERS?",self.lonely_numbers_check_all_linked(next_cell))
        print("SURROUNDED",self.smaller_surrounded_check_all())


        self.dump_both()
        print(self.cell_possibles)





    def build_up_givens(self):
        #check we already have a full solution saved in solution variable
        for row in self.solution:
            if 0 in row:
                raise Exception("Using build-up but solution is not complete")


        #START  by working out some "givens" - numbers that are given and pre-filled at the start
        self.givens= [[0 for c in range (self.cols)] for r in range(self.rows)]
        #these are a random pick from the original solution
        givens_to_give=5
        #print("DUMPING SOLUTION - SHOULDNT BE EMPTY")
        #self.dump_solution()

        build_up_log=[]   #use to report what we've done

        givens_added=0
        for g in range(givens_to_give):
            r=random.randint(0,self.rows-1)
            c=random.randint(0,self.cols-1)
            #print(f"GG R {r} C {c}")
            if self.givens[r][c]==0:
                self.givens[r][c]=self.solution[r][c]
                givens_added+=1

        #print(self.givens)
        build_up_log.append(f"Givens added {givens_added}")

        #NEXT let's see if this solution is unique - if not we need to add more givens

        try_no=0
        keep_going=True
        #self.first_trial_solution=self.solution

        while keep_going:
            try_no += 1
            self.solution=copy.deepcopy(self.givens)
            #print("Givens",self.givens)
            #self.dump_solution()
            self.initialise_cell_possibles(full_check=True)

            success= self.better_solver(multi=True)
            #TODO - only have one function and just tell it whether to do multi or not
            #success here means multiple solutions, fail = only one probably?
            if not success:
                keep_going = False
                if self.iteration_timeout:
                    raise Exception("**TIMED OUT IN BUILDUP**")
                else:
                    #print ("HOPEFULLY FINISHED? -- DIDN'T GET CLEAN SOLVE SECOND TIME")
                    keep_going=False

            else:
                #self.dump_solution()

                #ok, looks like solution is not unique
                #now work out where the two solutions are different

                diff = [[0 if self.first_trial_solution[r][c]==self.solution[r][c] else self.solution[r][c] for c in range (self.cols) ] for r in range(self.rows)]
                #print("DIFF",diff)

                #next up we need to add (at least) one of those differences to our givens and retry

                #TODO: could randomise this
                stop_rc_loop=False
                for r in range(self.rows):
                    for c in range(self.cols):
                        if self.first_trial_solution[r][c]!=self.solution[r][c]:
                            self.givens[r][c]=self.first_trial_solution[r][c]
                            build_up_log.append(f"added {r,c}")
                            stop_rc_loop=True
                            break
                    if stop_rc_loop:
                        break



        #reached end of While loop
        build_up_log.append(f"used {try_no} goes - so {try_no-1} extra givens")
        print(build_up_log)

        self.solution=self.first_trial_solution
        #METHOD END









    def lonely_numbers_check_all_linked(self,cell):
        linked_shapes=set()
        for linked in self.linked_cells:
            linked_shapes.add(self.get_shape(linked))
        for shape in linked_shapes:
            result=self.lonely_numbers_check_shape(shape)
            if result:
                return result

        return False, False

    def lonely_numbers_check_shape(self,shape_number):
        shape_cells=self.shape_cells[shape_number]
        #self.dump_both()
        for num in range(1,len(shape_cells)+1):
            count=0
            possibles_in_shape=[]
            last_found=False
            for cell in shape_cells:
                if self.get_solution(cell)==0:   #only check unsolved cells
                    possibles_in_shape.append((cell,self.cell_possibles[cell]))
                    if num in self.cell_possibles[cell]:
                        count+=1
                        last_found=cell
            if count==1:
                #print(f"found at cell {cell} size {len(shape_cells)} number {num} count {count}")
                return last_found,num

        return False

    def smaller_surrounded_check_all(self):
        #look at the shapes and see if any cells are completely surrounded by a shape (realistically 4 or less)
        #(meaning all cells of that shape touch them)
        #if so, can remove numbers 1-X (X=size)  from possibles list for those cells
        #size_override can be used to work for bigger shapes (only makes sense if you've already removed some possibles)
        removed=0
        for shape in self.shape_cells.values():
            if len(shape)>1 and len(shape)<5:
                broken_it,removed_list=self.surround_check_one_shape(shape)
                removed+=len(removed_list)

        return removed

    def surround_check_one_shape(self, shape, iterating=False, dumps=False):
        #TODO *****6/11/24
        #adding this function in has led to some puzzles showing as no solution, when they were being solved before - why?
        #(it does seem to speed things up in some cases though)

        # print (shape)
        match_all = set()
        removed_list=[]
        broken_it = False  #flag for  if removing possibles leaves to none left
        first_cell = True
        for cell in shape:
            if self.get_solution(cell)==0:  #only interested in blank cells (filled ones looked at elsewhere)
                linked = set(self.linked_cells[cell])
                neighbours_only = linked.difference(shape)
                if first_cell:
                    first_cell = False
                    match_all = neighbours_only
                else:
                    # keep tabs of cells that are connected to all shapes (so use intersection of sets)
                    match_all = match_all.intersection(neighbours_only)
                    if not match_all:
                        break  # no need to continue if the union is empty - won't be others that touch  all
        if match_all:
            # we have found one or more cells that is 'surrounded' - now remove possibles
            if dumps: print(f"matched - {shape}")
            shape_len=len(shape)
            if iterating:
                # print("!")
                numbers_to_remove=set(range(1,len(shape)+1)) #start with full set of numbers
                for c in shape:
                    if self.get_solution(c)!=0:
                        numbers_to_remove.remove(self.get_solution(c))
                        #er, bit confusing - remove from the remove list - ie one less number to remove from possibles
                # print(f"IT-SURR match {match_all} orig shape {shape} numbers to remove {numbers_to_remove} length {shape_len}")
            else:
                #if running at very start, just remove all numbers up to length of shape
                numbers_to_remove = range(1, len(shape)+1)
                # print(f"SURR match {match_all} orig shape {shape} length {shape_len}")

            for cell in match_all:
                for n in numbers_to_remove:
                    if n in self.cell_possibles[cell]:  #need to make sure cell is blank (as I leave the last possible in a completed cell)
                        if self.get_solution(cell)==0:
                            self.cell_possibles[cell].remove(n)
                            removed_list.append((cell,n))

                if not self.cell_possibles[cell]:
                    broken_it=True
                    return (broken_it,removed_list)

                    break

        return (False,removed_list)

    def is_whole_thing_valid(self):
        #double check the end solution is valid (Shouldn't really need)
        for r in range(self.rows):
            for c in range(self.cols):
                if not self._is_valid2(r,c,self.solution[r][c]):
                    print(f"Problem at ({r},{c}) with {self.solution[r][c]}")
                    return False
        return True






    def _is_valid2(self, row, col, num):
        #modifying Claude version to be more efficient and not fail if used after assignment
        # Check shape size
        shape = self.shapes[row][col]
        this_shape_cells = self.shape_cells[shape]
        shape_size = len(this_shape_cells)
        if num > shape_size:
            return False

        # Check if number already exists in shape
        for cell in this_shape_cells:
            if cell != (row,col) and self.get_solution(cell)==  num:
                #shape will included this cell, so don't trigger False just with that
                    return False

        # Check adjacent cells
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            nr, nc = row + dr, col + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols and self.solution[nr][nc] == num:
                return False

        #got this far, passed all checks
        return True





    #LESS USEFUL --



    def brute_force_solve(self):
        #This method and a few functions it uses were generated by Claude AI
        #but like Claude said, it is slow once you have anything but a small grid
        empty = self._find_empty()
        if not empty:
            return True  # Puzzle is solved

        self.iteration_counter+=1

        row, col = empty
        shape = self.shapes[row][col]
        shape_size = sum(row.count(shape) for row in self.shapes)

        for num in range(1, shape_size + 1):
            if self._is_valid2(row, col, num):
                self.solution[row][col] = num
                if self.brute_force_solve():
                    return True
                self.solution[row][col] = 0  # Backtrack

        return False

    def _find_empty(self):
        #claude for brute force
        for r in range(self.rows):
            for c in range(self.cols):
                if self.solution[r][c] == 0:
                    return (r, c)
        return None



#DUMPING GROUND -- DON'T THINK THIS STUFF IS SO USEFUL


    def _is_valid(self, row, col, num):
        #Claude for brute force
        # Check shape size
        shape = self.shapes[row][col]
        shape_size = sum(row.count(shape) for row in self.shapes)
        if num > shape_size:
            return False

        # Check if number already exists in shape
        for r in range(self.rows):
            for c in range(self.cols):
                if self.shapes[r][c] == shape and self.solution[r][c] == num:
                    return False

        # Check adjacent cells
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            nr, nc = row + dr, col + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols and self.solution[nr][nc] == num:
                return False

        return True


    def ac3(self):
        #from claude - don't yet understand
        queue = deque((X, Y) for X in self.cell_possibles for Y in self.linked_cells[X])
        while queue:
            X, Y = queue.popleft()
            if self._revise(X, Y):
                if len(self.cell_possibles[X]) == 0:
                    print("******FAILED AC3****")
                    return False
                other_affected_cells = (c  for c in self.linked_cells[X] if c!=Y)
                for Z in other_affected_cells:
                    queue.append((Z, X))
        return True

    def _revise(self, X, Y):
        revised = False
        for x in list(self.cell_possibles[X]):
            if not any(x != y for y in self.cell_possibles[Y]):
                self.cell_possibles[X].remove(x)
                print(f"REMOVING {x} from {X} and leaving {self.cell_possibles[X]}")
                revised = True
        return revised





#SIMPLE HELPER FUNCTIONS, NOT NEEDING TO BE PART OF A CLASS
def add_coords(coord1, coord2, offset=(0, 0)):
    return (coord1[0] + coord2[0] + offset[0], coord1[1] + coord2[1] + offset[1])



if __name__ == '__main__':
    print (sys.version)

    puzzle = Puzzle(7, 8)
    n=100
    keepgoing=True


    while keepgoing:




        random.seed(n)
        puzzle = Puzzle(7, 8)
        puzzle.iteration_timeout_limit = 10  # to allow for debugging
        puzzle.generate_grid_shapes()
        puzzle.generate_iteration_lookups()
        start_time = time.time()
        success = puzzle.better_solver(multi=False)
        print(n,success)
        if success:
            keepgoing=False
        else:
            n+=1

    puzzle.dump_both()

    puzzle.build_up_givens()
    puzzle.dump_both()
    print("double check", puzzle.is_whole_thing_valid())
    print(puzzle.givens)

    #now let's try to see if we can solve this using logic alone
    #first save the actual complete solution, and swap over to just the givens in the solution grid

    puzzle.original_solution=copy.deepcopy(puzzle.solution)
    puzzle.solution=copy.deepcopy(puzzle.givens)

    puzzle.logic_only_solver()


    quit()


    #MOSTLY WHAT FOLLOWS ARE LITLE EXPERIMENTS

    scores=defaultdict(int)
    overall_start_time=time.time()

    for n in range(1000):
        puzzle = Puzzle(7, 8)
        random.seed(100+n)
        puzzle.generate_grid_shapes()
        puzzle.generate_iteration_lookups()
        start_time=time.time()
        success = puzzle.better_solver(multi=False)
        result_to_print="none"
        if success:
            result_to_print="SOLUTION"
        elif puzzle.iteration_timeout:
            result_to_print="timeout"
        scores[result_to_print]+=1

        print(f"#{n} {result_to_print} {puzzle.iteration_counter} {time.time()-start_time}")


    print(scores)
    print("total time", time.time()-overall_start_time)

    quit()






    #puzzle=Puzzle(6,10)

    #print(puzzle.ALL_SHAPE_PERMUTATIONS)
    #puzzle.generate_grid_shapes()

    #fairly short and quick
    # puzzle = Puzzle(6, 5)
    # puzzle.shapes=[[7, 4, 5, 5, 5],[4, 4, 4, 2, 5],[6, 4, 2, 2, 2],[6, 6, 1, 2, 3],[6, 1, 1, 1, 3],[6, 8, 1, 3, 3]]

    #puzzle.shapes=[    [14, 3, 4, 4, 4, 4, 5, 6, 6, 7],     [3, 3, 3, 4, 2, 5, 5, 5, 6, 7],     [12, 3, 1, 2, 2, 2, 5, 8, 6, 7],    [12, 1, 1, 1, 2, 11, 8, 8, 6, 7],    [12, 12, 1, 10, 11, 11, 8, 9, 9, 7],     [13, 12, 10, 10, 10, 10, 8, 9, 9, 9] ]
    #puzzle.shapes=[    [13, 13, 3, 4, 4, 4, 4, 5, 6, 6],    [13, 3, 3, 3, 4, 2, 5, 5, 5, 6],    [12, 11, 3, 1, 2, 2, 2, 5, 7, 6],    [12, 11, 1, 1, 1, 2, 10, 7, 7, 6],    [12, 11, 11, 1, 9, 10, 10, 7, 8, 8],    [12, 12, 11, 9, 9, 9, 9, 7, 8, 8]]
    #puzzle.shapes=[[13, 13, 3, 4, 4, 4, 4, 5, 6, 6], [13, 3, 3, 3, 4, 2, 5, 5, 5, 6], [11, 12, 3, 1, 2, 2, 2, 5, 7, 6], [11, 12, 1, 1, 1, 2, 8, 8, 7, 6], [11, 10, 10, 1, 8, 8, 8, 9, 7, 7], [11, 11, 10, 10, 10, 9, 9, 9, 9, 7]]



    #this one takes about 15s and is unsolveable
    #puzzle = Puzzle(6, 10)
    #puzzle.shapes=[[5, 5, 3, 3, 3, 2, 11, 11, 11, 15], [5, 3, 3, 1, 2, 2, 2, 10, 11, 11], [5, 4, 1, 1, 1, 2, 10, 10, 10, 12], [4, 4, 4, 1, 9, 9, 8, 10, 12, 12], [7, 4, 6, 6, 6, 8, 8, 8, 12, 13], [7, 7, 7, 7, 6, 6, 8, 14, 12, 13]]

    #random.seed(11)
    puzzle = Puzzle(6,8)
    puzzle.generate_grid_shapes()

    #nice example - brute force = 0.5mil, better= 0.48 mil,  better+ lonely=57 iterations!
    #puzzle.shapes=[[4, 4, 3, 3, 3, 9, 9, 9], [4, 3, 3, 2, 9, 9, 10, 10], [4, 1, 2, 2, 2, 8, 8, 8], [1, 1, 1, 2, 8, 8, 7, 11], [6, 1, 5, 5, 5, 7, 7, 7], [6, 6, 6, 6, 5, 5, 7, 12]]




    print(puzzle.shapes)
    print()
    puzzle.dump_shapes()
    print()
    puzzle.generate_iteration_lookups()
    # puzzle.dump_both()


    # #BRUTE FORCE FIRST
    # puzzle.iteration_counter = 0
    # start_time=time.time()
    # puzzle.brute_force_solve()
    # puzzle.dump_solution()
    # print("time taken - brute force", round(time.time()-start_time,3))
    # print("VALID?", puzzle.is_whole_thing_valid())
    # print(f"iterations {puzzle.iteration_counter:,}")
    # print()

    # puzzle.clear_solution()
    # puzzle.iteration_counter = 0
    # start_time = time.time()
    # success= puzzle.better_solver()
    # puzzle.dump_solution()
    # print("time taken - better",round(time.time()-start_time,3))
    # print("VALID?",puzzle.is_whole_thing_valid())
    # print("part time",puzzle.iterate_part_timer)
    # print(f"iterations {puzzle.iteration_counter:,}")
    # print()

    puzzle.clear_solution()
    puzzle.initialise_cell_possibles()
    # puzzle.dump_both()
    puzzle.iteration_counter=0
    puzzle.iterate_part_timer = 0
    start_time = time.time()
    success= puzzle.better_solver(use_lonely=True)
    puzzle.dump_solution()
    print("time taken - better + lonely",round(time.time()-start_time,3))
    print("VALID?",puzzle.is_whole_thing_valid())
    print("part time",puzzle.iterate_part_timer)
    print(f"iterations {puzzle.iteration_counter:,}")
    print()
    print()

    if not success:
        exit()

    # NOW TRY WITH UNIQUENESS SOLVER  --- BUILD METHOD
    start_time = time.time()
    puzzle.build_up_givens()
    print("time taken - BUILD", round(time.time() - start_time, 3))
    print("VALID?", puzzle.is_whole_thing_valid())
    print("part time", puzzle.iterate_part_timer)
    print(f"iterations {puzzle.iteration_counter:,}")


    exit()

    #NOW TRY WITH UNIQUENESS SOLVER
    puzzle.clear_solution()
    puzzle.initialise_cell_possibles()
    # puzzle.dump_both()
    puzzle.iteration_counter = 0
    puzzle.iterate_part_timer = 0
    start_time = time.time()
    success = puzzle.better_solver(use_lonely=True)
    print("Success?", success)
    puzzle.dump_solution()
    print("time taken - UNIQUENESS", round(time.time() - start_time, 3))
    print("VALID?", puzzle.is_whole_thing_valid())
    print("part time", puzzle.iterate_part_timer)
    print(f"iterations {puzzle.iteration_counter:,}")



