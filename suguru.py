# Suguru test
""""

trying to create a suguru puzzle
"""

import turtle
import numpy as np

# SETUP
num_cols = 13
num_rows = 10
cell_draw_size = 35

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
        this_shape=grid_shapes[r,c]
        this_shape_coords = shape_coords.get(this_shape)
        if not this_shape_coords:
            this_shape_coords = []
        this_shape_coords.append((r,c))
        shape_coords[this_shape] = this_shape_coords

print (shape_coords)




screen = turtle.Screen()
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
print(grid.shape)

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

pen.left(90)
pen.up()
pen.setpos(start_coords)
horiz_offset=cell_draw_size / 2
pen.forward(horiz_offset) #centre horizontally
pen.right(90)
vert_offset = cell_draw_size * .9
pen.forward(vert_offset) #vertical adjustment
pen.left(90)

# now numbers
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

#input("presss enter to go further")


# SOLVING

# Check If Shape Has Just 1 Number missing

found=0 #keep a count of how many found
for shape_number,shape in shape_coords.items():
    # print(shape)
    shape_size=len(shape)
    blank_cells = 0

    for cell in shape:
        if grid[cell]==0:
            blank_cells +=1
            last_blank=cell

    # print ("Shape Number", shape_number, "Size/Blanks", shape_size, blank_cells)
    if blank_cells == 1 :
        found+=1
        print ("Shape Number", shape_number, "Size/Blanks", shape_size, blank_cells)
        # now let's work out what it should be
        numbers_needed=list(range(1,shape_size+1))
        print ("numbers needed", numbers_needed)
        for cell in shape:
            if grid[cell]==0:
                blank_posn=cell
            else:
                numbers_needed.remove(grid[cell])
        #numbers_needed[0] should now have the missing number
            missing_value=numbers_needed[0]
            print("missing",missing_value)
            print("cell location",blank_posn)


            def display_newnumber(num, rc_tuple):
                xpos = start_coords[0] + cell_draw_size * rc_tuple[1] + horiz_offset
                ypos = start_coords[1] - cell_draw_size * rc_tuple[0] - vert_offset  # down is negative
                pen.setpos(xpos, ypos)
                pen.color("blue")
                pen.write(num, align="center", font=("Comic Sans MS", 18, "normal"))
                print("number =", grid[r, c])


            grid[blank_posn]=missing_value
            display_newnumber(missing_value,blank_posn)

        # TODO -- array of which numbers are original
        # now display any  new number(s) found


#Check if any cells have all but one number neighbouring
found=0
for r in range(num_rows):
    for c in range(num_cols):
        if grid[r,c]==0: #only check for blanks
            numbers_available=list(range(1,6))
            # get neighbours
            neighbours=[]
            for nb_r in range(r-1,r+2):
                if 0<=nb_r<=num_rows-1:
                    for nb_c in range(c-1,c+2):
                        if 0<=nb_c <=  num_cols-1:
                            neighbours.append((nb_r,nb_c))
            neighbours.remove((r,c)) #don't include itself

            for nb in neighbours:
                if grid[nb] in numbers_available:
                    numbers_available.remove(grid[nb])


            print("Cell: ",r,c, "Numbers Available",len(numbers_available),":",numbers_available,"Neighbours",len(neighbours),neighbours)
            if len(numbers_available)==1:  #found one!
                print ("FOUND ONE!")
                found+=1
                grid[r,c]=numbers_available[0]
                display_newnumber(numbers_available[0],(r,c))








        # tick off numbers in neighbours

        # see how many numbers are left







# loop through all shapes
# check if shape has only 1 missing number


turtle.done()

# pen.showturtle()


'''
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
'''
