#Puzzle
#This file aiming to refactor suguru into a tidier, class based approach

import random, time, json, pprint

class Puzzle:


    def __init__(self,rows,cols):
        #set dimensions of puzzle
        self.rows=rows
        self.cols=cols

        #now create two blank (filled with zero) grids:
        self.values= [[0 for c in range (cols)] for r in range(rows)]   #values ie only 1-5 possible, in each cell
        self.shapes= [[0 for c in range (cols)] for r in range(rows)]   #shape number that cell belongs to - defines shapes within the grid

        #load the lookup table of all possible shapes and their permutations
        #this has been previously generated from trial and error - and then doing a rotation of each etc - see gridgenerate create shape permutations and translate shapes
        #should stay a constant throughout
        self.ALL_SHAPE_PERMUTATIONS=self.load_all_shape_permutations()

    def load_all_shape_permutations(self):
        with open("shape_permutations.json", 'r') as f:
            tempdict = json.load(f)
        return tempdict



    def in_bounds(self,coord):
        valid = (0 <= coord[0] <= self.rows - 1) and (0 <= coord[1] <= self.cols - 1)
        return valid

    def get_value(self,coord):
        return self.values[coord[0]][coord[1]]

    def get_shape(self,coord):
        return self.shapes[coord[0]][coord[1]]

    def set_value(self,coord,value):
        self.values[coord[0]][coord[1]]=value

    def set_shape(self,coord,value):
        self.shapes[coord[0]][coord[1]]=value

    def dump_values(self):
        for row in self.values:
            print(row)

    def dump_shapes(self):
        for row in self.shapes:
            print(row)


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
        verbose=True
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


            print ("valid?", valid)

            if valid:
                for coord in shape_to_try:
                    adjusted_coord = add_coords(coord, active_point, home_coord_offset)
                    self.set_shape(adjusted_coord,shape_number)
            self.dump_shapes()
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



'''
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
                    # if verbose: print(f"not found valid shape possibility, coord={new_point}")
                    print(
                        f"not found valid shape possibility, coord={new_point}")  # this shouldn't really happen should it?

'''


def add_coords(coord1, coord2, offset=(0, 0)):
    return (coord1[0] + coord2[0] + offset[0], coord1[1] + coord2[1] + offset[1])



if __name__ == '__main__':
    puzzle=Puzzle(8,5)
    print(puzzle.values)
    print(puzzle.ALL_SHAPE_PERMUTATIONS)
    puzzle.generate_grid_shapes()



