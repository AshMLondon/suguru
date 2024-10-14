#Puzzle
#This file aiming to refactor suguru into a tidier, class based approach

import random, time, json
from pprint import pprint
import sys
from collections import defaultdict, deque

class Puzzle:


    def __init__(self,rows,cols):
        #set dimensions of puzzle
        self.rows=rows
        self.cols=cols

        self.iterate_part_timer=0

        #now create two blank (filled with zero) grids:
        #self.values= [[0 for c in range (cols)] for r in range(rows)]   #values ie only 1-5 possible, in each cell
        self.solution= [[0 for c in range (cols)] for r in range(rows)]   #values ie only 1-5 possible, in each cell
        self.shapes= [[0 for c in range (cols)] for r in range(rows)]   #shape number that cell belongs to - defines shapes within the grid

        #load the lookup table of all possible shapes and their permutations
        #this has been previously generated from trial and error - and then doing a rotation of each etc - see gridgenerate create shape permutations and translate shapes
        #should stay a constant throughout
        self.ALL_SHAPE_PERMUTATIONS=self.load_all_shape_permutations()

    def load_all_shape_permutations(self):
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
        for row in self.solution:
            print(row)

    def dump_shapes(self):
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

            #print(self.shapes[r],"   ",self.solution[r]," ... ",poss)
            print( self.solution[r], " ... ", poss)
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

    def color_shapes(self):
        shape_colors = {}
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
            adjacent_colors = {shape_colors[adj] for adj in adjacent_shapes if adj in shape_colors}
            for color in range(1, 7):  # We only need to check up to 4 colors #yeah, but it's a bit boring!!
                if color not in adjacent_colors:
                    shape_colors[shape] = color
                    break


        self.shape_colours=shape_colors
        return shape_colors


    def generate_grid_shapes(self):
        #function to generate a full grid of shapes - based on pre-loaded shapes (and permutations)

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

        keep_going=True
        while keep_going:

            if verbose: print(f"Goes {go} Active Point",active_point)

            for shape_name, shape_permutations in self.ALL_SHAPE_PERMUTATIONS:
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

                            ''' 
                            #single cell stop stuff - can add in later    
                            if single_cell_stop:
                                    if valid:
                                        # first establish affected cells
                                        affected_cells = set()
                                        shape_try_adjusted = []
                                        for coord in shape_to_try:
                                            adjusted_coord = add_coords(coord, new_point, home_coord_offset)
                                            shape_try_adjusted.append(adjusted_coord)
                                            affected_cells.update(get_sideways_neighbours(adjusted_coord))
    
                                        for coord in affected_cells:
                                            if coord not in shape_try_adjusted and grid_shapes[
                                                coord] == 0:  # don't check members of prospective shape itself and affected cell needs to be empty
                                                sideways_neighbours = get_sideways_neighbours(coord)
                                                empty_before_shape = 0
                                                empty_after_shape = 0
                                                # logic that follows - we need affected shapes to have at least 1 blank - after the shape has gone in (if had 0 before that's ok)
                                                for nb in sideways_neighbours:
                                                    if grid_shapes[nb] == 0:
                                                        empty_before_shape += 1
                                                        if nb not in shape_try_adjusted:
                                                            empty_after_shape += 1
                                                if empty_after_shape == 0 and empty_before_shape != 0:
                                                    single_cell_count += 1
                                                    if single_cell_count > single_cell_max:  # allow *some*
                                                        # TODO check how close?
                                                        valid = False
                                                        # print (f"**single cell**  affected cell {coord} -- emptybefore  {empty_before_shape}  emptyafter {empty_after_shape}")
                                                        break
    
                                        # print (f"shape number {shape_number}-- valid {valid} -- shape coords {shape_try_adjusted} ** affected cells: {affected_cells}")
                            '''

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

    def initialise_cell_possibles(self):
        #generate dict of all possible values at each shape [aka "the domain"]
        self.cell_possibles={}
        for r in range(self.rows):
            for c in range (self.cols):
                self.cell_possibles[(r,c)]=set(range(1,len(self.shape_cells[self.shapes[r][c]])+1))
                #work out possibles by seeing how many cells in the r,c shape - generate a list starting with 1 up to that number and store in dictionary at r,c

    def pick_next_empty_cell(self):
        #function to find the next cell to iterate - which cell is empty and has fewest possible values
        #using Claude's list comprehension - hopefully is efficient
        starting_time_here=time.time()
        #return min((cell for cell in self.cell_possibles if self.solution[cell[0]][cell[1]] == 0), key=lambda cell: len(self.cell_possibles[cell]),default=False)
        next_cell= min((cell for cell in self.cell_possibles if self.solution[cell[0]][cell[1]] == 0), key=lambda cell: len(self.cell_possibles[cell]),default=False)
        self.iterate_part_timer+=(time.time()-starting_time_here)
        return next_cell


    def generate_iteration_lookups(self):
        #create all lookups needed to run iteration -- order is important as later ones depend on first
        self.generate_shape_cells()
        self.generate_linked_cells()
        self.initialise_cell_possibles()

    def better_solver(self,next=False):
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

        if next:  #if the next cell has already been given as a parameter
            live_cell=next
        else:
            live_cell=self.pick_next_empty_cell()
        #print(f"Next= {live_cell}")
        if not live_cell:  #if there is no live cell returned, that's because we've done them all
            return True

        #now start to loop  through all possible values for that cell

        for num in self.cell_possibles[live_cell]:
            #set the value
            self.set_solution(live_cell,num)
            #self.dump_both()

            #now let's see what impact that has, now we've added another number
            #pull list of impacted cells - same shape + neighbours
            changes_made=[]
            broken_it=False
            single_location=False
            for linked in self.linked_cells[live_cell]:
                #go through them all - if any are same value, remove that value, but note which cell we're removing from
                if num in self.cell_possibles[linked]:
                    self.cell_possibles[linked].remove(num)
                    #if len(self.cell_possibles[linked])==1:
                    #    single_location=linked
                    #tried this to speed up, but actually slightly slowed down by checking this too often
                    changes_made.append((linked,num))
                    if not self.cell_possibles[linked]:
                        broken_it=True
                        break
                        #if we've got no possible left, that's wrong, stop this process

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
                success=self.better_solver(next=single_location)
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







    def brute_force_solve(self):
        #This method and a few functions it uses were generated by Claude AI
        #but like Claude said, it is slow once you have anything but a small grid
        empty = self._find_empty()
        if not empty:
            return True  # Puzzle is solved

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



    def is_whole_thing_valid(self):
        #doesnt really work as cell itself triggers a problem
        #also is valid v wasteful - looks at whole grid to check the shape
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

    def _find_empty(self):
        #claude for brute force
        for r in range(self.rows):
            for c in range(self.cols):
                if self.solution[r][c] == 0:
                    return (r, c)
        return None

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
                print(f"REMOVING {x} from {X}")
                revised = True
        return revised





#SIMPLE HELPER FUNCTIONS, NOT NEEDING TO BE PART OF A CLASS
def add_coords(coord1, coord2, offset=(0, 0)):
    return (coord1[0] + coord2[0] + offset[0], coord1[1] + coord2[1] + offset[1])



if __name__ == '__main__':
    print (sys.version)
    #puzzle=Puzzle(6,10)

    #print(puzzle.ALL_SHAPE_PERMUTATIONS)
    #puzzle.generate_grid_shapes()

    #fairly short and quick
    #puzzle = Puzzle(6, 5)
    #puzzle.shapes=[[7, 4, 5, 5, 5],[4, 4, 4, 2, 5],[6, 4, 2, 2, 2],[6, 6, 1, 2, 3],[6, 1, 1, 1, 3],[6, 8, 1, 3, 3]]

    #puzzle.shapes=[    [14, 3, 4, 4, 4, 4, 5, 6, 6, 7],     [3, 3, 3, 4, 2, 5, 5, 5, 6, 7],     [12, 3, 1, 2, 2, 2, 5, 8, 6, 7],    [12, 1, 1, 1, 2, 11, 8, 8, 6, 7],    [12, 12, 1, 10, 11, 11, 8, 9, 9, 7],     [13, 12, 10, 10, 10, 10, 8, 9, 9, 9] ]
    #puzzle.shapes=[    [13, 13, 3, 4, 4, 4, 4, 5, 6, 6],    [13, 3, 3, 3, 4, 2, 5, 5, 5, 6],    [12, 11, 3, 1, 2, 2, 2, 5, 7, 6],    [12, 11, 1, 1, 1, 2, 10, 7, 7, 6],    [12, 11, 11, 1, 9, 10, 10, 7, 8, 8],    [12, 12, 11, 9, 9, 9, 9, 7, 8, 8]]
    #puzzle.shapes=[[13, 13, 3, 4, 4, 4, 4, 5, 6, 6], [13, 3, 3, 3, 4, 2, 5, 5, 5, 6], [11, 12, 3, 1, 2, 2, 2, 5, 7, 6], [11, 12, 1, 1, 1, 2, 8, 8, 7, 6], [11, 10, 10, 1, 8, 8, 8, 9, 7, 7], [11, 11, 10, 10, 10, 9, 9, 9, 9, 7]]



    #this one takes about 15s and is unsolveable
    puzzle = Puzzle(6, 10)
    puzzle.shapes=[[5, 5, 3, 3, 3, 2, 11, 11, 11, 15], [5, 3, 3, 1, 2, 2, 2, 10, 11, 11], [5, 4, 1, 1, 1, 2, 10, 10, 10, 12], [4, 4, 4, 1, 9, 9, 8, 10, 12, 12], [7, 4, 6, 6, 6, 8, 8, 8, 12, 13], [7, 7, 7, 7, 6, 6, 8, 14, 12, 13]]

    print(puzzle.shapes)
    print()
    puzzle.dump_shapes()
    print()


    print()

    puzzle.generate_iteration_lookups()
    puzzle.dump_both()

    start_time = time.time()
    success=puzzle.better_solver()
    puzzle.dump_solution()
    print("time taken - better",round(time.time()-start_time,3))
    print("VALID?",puzzle.is_whole_thing_valid())
    print("part time",puzzle.iterate_part_timer)

    puzzle.clear_solution()
    puzzle.initialise_cell_possibles()

    puzzle.dump_both()


    start_time = time.time()
    puzzle.ac3()
    print("AC3",round(time.time()-start_time,3))

    start_time = time.time()
    success=puzzle.better_solver()
    puzzle.dump_solution()
    print("time taken - better",round(time.time()-start_time,3))
    print("VALID?",puzzle.is_whole_thing_valid())
    print("part time",puzzle.iterate_part_timer)

    exit()

    start_time=time.time()
    puzzle.clear_solution()
    puzzle.brute_force_solve()
    puzzle.dump_solution()
    print("time taken - brute force", round(time.time()-start_time,3))
    print("VALID?", puzzle.is_whole_thing_valid())




    exit()


    puzzle.brute_force_solve()
    puzzle.dump_solution()
    puzzle.clear_solution()


    start_time=time.time()
    puzzle = Puzzle(8, 5)
    puzzle.generate_grid_shapes()
    puzzle.dump_shapes()
    print (f"time to generate grid {round(time.time()-start_time,3)}")
    puzzle.brute_force_solve()
    print (f"time to solution {round(time.time()-start_time,3)}")
    puzzle.dump_solution()

