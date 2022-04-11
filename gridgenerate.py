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

grid=np.zeros((num_rows, num_cols), dtype=int)
grid_shapes=np.zeros((num_rows, num_cols), dtype=int)


screen = turtle.Screen()
screen.delay(0)
screen.tracer(1)

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

def blank_out_grid():
    for r in range(num_rows):
        for c in range(num_cols):
            fill_cell((r,c),"white")


def generate_empty_grid():
    ######START GENERATING NEW GRID
    start_point = (5, 5)
    this_point = start_point
    move_coord = [(-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)]
    # colours=["orange","blue","green","cyan","magenta","pink","red","olive","orchid","seagreen","yellow"]
    shape_number = 1
    while shape_number < 90:  # 90 is just in case it goes horribly wrong
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

        print("shape: ", shape_number, "length: ", length, "tries: ", tries)  # this_shape)
        if length:
            for cell in this_shape:
                grid_shapes[cell] = shape_number
            shape_number += 1
            # print (grid_shapes)
            time.sleep(0.01)

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
                print("****finished?")
                break

    return grid_shapes


generate_empty_grid()
print(grid_shapes)
blank_out_grid()
draw_grid()

#shape_coords=create_shape_dict()

'''
#ok, let's throw in some random numbers
for i in range(9):
    shape=random.choice(list(shape_coords.items()))
    shape_size=len(shape)
    cell=random.choice(shape)
    grid_shapes[cell]=random.randint(1,shape_size)

'''










if __name__ == '__main__':
    turtle.done()

