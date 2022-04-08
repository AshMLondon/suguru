# Suguru test
""""

trying to create a suguru puzzle
"""

import numpy as np
import turtle

##INITIALISE
num_cols=13
num_rows=10

#grid=np.zeros((num_rows, num_cols), dtype=int)
#grid_shapes=np.zeros((num_rows, num_cols), dtype=int)


numbers_given_CSV=[
[0,0,0,0,0,0,0,0,0,0,0,4,0],
[0,0,0,5,3,1,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,3,2,0],
[0,0,0,0,0,0,0,5,3,0,4,0,0],
[0,3,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,3,0],
[0,0,0,0,0,0,0,0,0,0,5,0,0],
[0,0,1,0,0,0,3,0,2,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0]
]

shape_as_CSV=[
[1,1,1,2,3,3,3,4,4,4,5,6,6],
[7,8,2,2,2,9,3,3,10,5,5,5,6],
[7,8,8,2,9,9,9,10,10,10,5,11,6],
[7,7,8,12,12,9,13,13,10,14,11,11,6],
[15,7,16,16,12,12,12,13,14,14,11,11,17],
[15,15,16,16,16,18,19,13,13,14,14,17,17],
[15,20,20,20,18,18,18,21,22,22,23,17,24],
[25,25,20,26,26,18,21,21,21,23,23,23,24],
[25,25,20,27,26,26,26,21,28,28,23,24,24],
[27,27,27,27,29,29,29,29,28,28,28,24,30],
]


grid=np.array(numbers_given_CSV)
grid_shapes= np.array(shape_as_CSV)




screen=turtle.Screen()
#screen.bgcolor("orange")
screen.delay(0)
screen.tracer(0)


pen=turtle.Turtle()
pen.speed(0)
#pen.hideturtle()
cell_draw_size = 40
start_coords=(-screen.window_width()/2+cell_draw_size,screen.window_height()/2-cell_draw_size)


row_width= cell_draw_size * (num_cols-1)
line_light=1
line_heavy=3

pen.up()
#pen.setpos(-row_width, +row_width)
pen.setpos(start_coords)
pen.down()
print (grid.shape)

#draw rows
for r in range(num_rows+1):
    for c in range(num_cols):
        pen.width(line_light)
        if r==0: pen.width(line_heavy)
        elif r==num_rows:
            pen.width(line_heavy)
        else:
            if grid_shapes[r-1,c]!=grid_shapes[r,c]: pen.width(line_heavy)
        pen.forward(cell_draw_size)
    pen.right(90)
    pen.up()
    pen.forward(cell_draw_size)
    pen.left(90)
    pen.backward(row_width+cell_draw_size)
    pen.down()

#now columns
pen.up()
pen.setpos(start_coords)
pen.down()
pen.right(90)
for c in range(num_cols+1):
    for r in range(num_rows):
        pen.width(line_light)
        if c==0: pen.width(line_heavy)
        elif c==num_cols:
            pen.width(line_heavy)
        else:
            if grid_shapes[r,c-1]!=grid_shapes[r,c]: pen.width(line_heavy)
        pen.forward(cell_draw_size)
    pen.left(90)
    pen.up()
    pen.forward(cell_draw_size)
    pen.right(90)
    pen.backward(cell_draw_size*(num_rows))
    pen.down()

pen.left(90)
pen.up()
pen.setpos(start_coords)
pen.forward(cell_draw_size/2)
pen.right(90)
pen.forward(cell_draw_size*.9)
pen.left(90)

#now numbers
for r in range(num_rows):
    for c in range(num_cols):
        if grid[r,c] != 0:
            pen.write(grid[r,c],align="center", font=("Arial", 20, "normal"))
        pen.forward(cell_draw_size)
    pen.right(90)
    pen.forward(cell_draw_size)
    pen.left(90)
    pen.backward(row_width+cell_draw_size)




turtle.done()


#pen.showturtle()




'''
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
'''