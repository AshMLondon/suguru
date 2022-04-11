# Grid Generate
""""
Suguru Puzzle Grid Generator -- trial

by Ashley,  April 2022
"""




import turtle, time, random
import numpy as np



# SETUP
num_cols = 13
num_rows = 10
cell_draw_size = 40
horiz_offset = cell_draw_size / 2
vert_offset = cell_draw_size * .9
row_width = cell_draw_size * (num_cols - 1)
display_build=False #show shapes  building up slowly, or jump in one go

grid=np.zeros((num_rows, num_cols), dtype=int)
grid_shapes=np.zeros((num_rows, num_cols), dtype=int)


screen = turtle.Screen()
screen.delay(0)
screen.tracer(0)
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


draw_grid()


def random_colour():
    colour="#"
    for i in range(3):
        colour=colour+hex(random.randint(128,240))[-2:]
    return colour

def fill_cell(coord,colour="orange"):
    c,r=coord
    pen.setpos(start_coords[0]+r*cell_draw_size,start_coords[1]-c*cell_draw_size)
    pen.fillcolor(colour)
    pen.setheading(0) #east
    pen.begin_fill()
    for i in range(4):
        pen.forward(cell_draw_size)
        pen.right(90)
    pen.end_fill()



######START HERE

start_point=(5,5)

this_point=start_point
#moves=["up","down","left","right"]
move_coord=[(-1,0),(1,0),(0,-1),(0,1),(0,0)]
colours=["orange","blue","green","cyan","magenta","pink","red","olive","orchid","seagreen","yellow"]

for shape_number in range(90):
    this_shape = []
    length = 0
    #colour=colours[shape_number%len(colours)]
    colour=random_colour()
    #colour=(random.randint(5,95),random.randint(5,95),random.randint(0,95))
    keep_going=True
    tries=0
    while keep_going:
        choice=random.randint(0,4)
        move=move_coord[choice]
        new_point = tuple(np.add(this_point,move))

        #check valid
        valid=True
        if not(0 <= new_point[0] <= num_rows-1): valid=False
        if not (0 <= new_point[1] <= num_cols-1): valid = False
        if valid and grid_shapes[new_point]>0: valid=False

        if valid:
            this_point=new_point
            if this_point not in this_shape:
                this_shape.append(this_point)
                fill_cell(this_point,colour)
                length+=1
            if length==5: keep_going=False
        else:
            if length==0 and tries>999995:
                this_point=new_point
                print("stuck",this_point)

        tries+=1
        if tries>35: keep_going=False

    print("shape: ",shape_number, "length: ",length, "tries: ",tries) #this_shape)
    for cell in this_shape:
        grid_shapes[cell]=shape_number
    #print (grid_shapes)
    if display_build:  time.sleep(0.2)

    if this_shape==[]:
        print("bit stuck")
        #bit stuck - find some blank space to go back to
        empty_cell=[]
        for r in range(num_rows):
            if empty_cell: break
            for c in range(num_cols):
                if grid_shapes[r,c]==0:
                    empty_cell=(r,c)
                    print("stuck outcome:",empty_cell)
                    break
        if empty_cell:
            this_point=empty_cell
        else:
            #we've finished
            print("****finished?")
            break

print(grid_shapes)
draw_grid()


shape_coords = {}
for r in range(num_rows):
    for c in range(num_cols):
        this_shape = grid_shapes[r, c]
        this_shape_coords = shape_coords.get(this_shape)
        if not this_shape_coords:
            this_shape_coords = []
        this_shape_coords.append((r, c))
        shape_coords[this_shape] = this_shape_coords


#Ok, let's try to solve with a recursive function to make sure it's possible
#let's do this one shape by shape shall we

def display_newnumber(num, rc_tuple, colour="blue"):
    xpos = start_coords[0] + cell_draw_size * rc_tuple[1] + horiz_offset
    ypos = start_coords[1] - cell_draw_size * rc_tuple[0] - vert_offset  # down is negative
    pen.setpos(xpos, ypos)
    pen.color(colour)
    pen.write(num, align="center", font=("Comic Sans MS", 18, "normal"))


def get_neighbours(r, c):
    neighbours = []
    for nb_r in range(r - 1, r + 2):
        if 0 <= nb_r <= num_rows - 1:
            for nb_c in range(c - 1, c + 2):
                if 0 <= nb_c <= num_cols - 1:
                    neighbours.append((nb_r, nb_c))
    neighbours.remove((r, c))  # don't include itself
    return neighbours



def iterate(cell_iter_no,num_to_try):
    print (cell_iter_no)
    success=False
    r=cell_iter_no//num_cols
    c=cell_iter_no%num_cols
    shape_no=grid_shapes[(r,c)]
    shapes=shape_coords[shape_no]
    max_nums=len(shapes)

    #try this number
    grid[r,c]=num_to_try

    #now let's check if valid
    valid=True
    for shape in shapes:
        if shape!=(r,c) and grid[shape]==num_to_try:
            valid=False
    neighbours=get_neighbours(r,c)
    for nb in neighbours:
        if grid[nb]==num_to_try:
            valid=False

    #if ok
    if valid:
        cell_iter_no+=1
        if cell_iter_no<30: #num_rows*num_cols:
            iterate(cell_iter_no,1)
        else:
            success=True
    else: #not valid
        if num_to_try<max_nums:
            num_to_try+=1
            iterate(cell_iter_no,num_to_try)
        else:
            grid[r,c]=0
            #exit the iteration

    return(success)






cell_iter_no=0
num_to_try=1
iterate(cell_iter_no,num_to_try)

print("hello!!")


print(grid)




# now numbers
pen.left(90)
pen.up()
pen.setpos(start_coords)
horiz_offset = cell_draw_size / 2
vert_offset = cell_draw_size * .9
pen.forward(horiz_offset)  # centre horizontally
pen.right(90)

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


turtle.done()

