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



if __name__ == '__main__':
    puzzle=Puzzle(6,4)
    print(puzzle.values)
    print(puzzle.ALL_SHAPE_PERMUTATIONS)
