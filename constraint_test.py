from constraint import *
import  time, sys
from puzzle import Puzzle

print (sys.version)



'''
problem = Problem()
#problem.addVariable("a", [1,2,3])
# problem.addVariable("b", [4,5,6])

rows=3
cols=3
shapes=[[(0,0)],[(0,1),(1,1),(1,0)],[(0,2),(1,2),(2,2),(2,1),(2,0)]]

for r in range(rows):
    for c in range(cols):
        problem.addVariable((r,c),range(20))

#problem.addConstraint(AllDifferentConstraint(),[(0,0),(1,1),(2,2)])

for shape in shapes:
    problem.addConstraint(AllDifferentConstraint(),shape)
#problem.addConstraint()

move_directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
for r in range(rows):
    for c in range(cols):
        for move_r, move_c in move_directions:
            new_r, new_c = r + move_r, c + move_c
            if 0 <= new_r < rows and 0 <= new_c < cols:
                if (r,c)<(new_r,new_c):
                    #print(f"RC {r,c} new {new_r,new_c}")
                    problem.addConstraint(AllDifferentConstraint(), [(r,c),(new_r,new_c)])

solution=problem.getSolution()
print(solution)
print()


for r in range(rows):
    line=(list(solution[(r,c)] for c in range(cols)))
    print (line)
'''


#START AGAIN
problem = Problem()
print (problem.getSolver())

puzzle = Puzzle(6, 5)
puzzle.shapes=[[7, 4, 5, 5, 5],[4, 4, 4, 2, 5],[6, 4, 2, 2, 2],[6, 6, 1, 2, 3],[6, 1, 1, 1, 3],[6, 8, 1, 3, 3]]

#puzzle = Puzzle(6, 10)
#puzzle.shapes=[[5, 5, 3, 3, 3, 2, 11, 11, 11, 15], [5, 3, 3, 1, 2, 2, 2, 10, 11, 11], [5, 4, 1, 1, 1, 2, 10, 10, 10, 12], [4, 4, 4, 1, 9, 9, 8, 10, 12, 12], [7, 4, 6, 6, 6, 8, 8, 8, 12, 13], [7, 7, 7, 7, 6, 6, 8, 14, 12, 13]]

rows, cols = puzzle.rows, puzzle.cols

puzzle.generate_shape_cells()

start_time=time.time()
#add variables based on r,c and the size of the shape there
for r in range(rows):
    for c in range(cols):
        problem.addVariable((r,c),range(1,len(puzzle.shape_cells[puzzle.shapes[r][c]])+1))
        #problem.addVariable((r,c),range(1,6))

#add constraint all cells in shape must be different
for shape in puzzle.shape_cells.values():
    problem.addConstraint(AllDifferentConstraint(),shape)

#add constraint that  adjoining neighbours must be different (only need this 1 way)
move_directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
for r in range(rows):
    for c in range(cols):
        for move_r, move_c in move_directions:
            new_r, new_c = r + move_r, c + move_c
            if 0 <= new_r < rows and 0 <= new_c < cols:
                if (r,c)<(new_r,new_c):
                    #print(f"RC {r,c} new {new_r,new_c}")
                    problem.addConstraint(AllDifferentConstraint(), [(r,c),(new_r,new_c)])


solution=problem.getSolution()
print(solution)
print()

print ("time taken",time.time()-start_time)
for r in range(rows):
    line=(list(solution[(r,c)] for c in range(cols)))
    print (line)
