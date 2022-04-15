# Grid Generate
""""
Suguru Puzzle Grid Generator -- trial

by Ashley,  April 2022
"""




import turtle, time, random
import numpy as np


verbose=False
max_iters = 200000

# TODO: spot fatal shapes -- C shape and big right angle, and skip if they happen
# TODO: change recursion to iteration and see if that speeds things up


# SETUP
num_cols = 13 #13
num_rows = 10 #10
cell_draw_size = 40
horiz_offset = cell_draw_size / 2
vert_offset = cell_draw_size * .9
row_width = cell_draw_size * (num_cols - 1)
display_build=False #show shapes  building up slowly, or jump in one go


grids_tried=0
found_one_yet=False

while not found_one_yet:

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



    random_gen=True

    if random_gen:

        ######START GENERATING RANDOM GRID HERE

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

            #print("shape: ",shape_number, "length: ",length, "tries: ",tries) #this_shape)
            for cell in this_shape:
                grid_shapes[cell]=shape_number
            #print (grid_shapes)
            if display_build:  time.sleep(0.2)

            if this_shape==[]:
                #print("bit stuck")
                #bit stuck - find some blank space to go back to
                empty_cell=[]
                for r in range(num_rows):
                    if empty_cell: break
                    for c in range(num_cols):
                        if grid_shapes[r,c]==0:
                            empty_cell=(r,c)
                            #print("stuck outcome:",empty_cell)
                            break
                if empty_cell:
                    this_point=empty_cell
                else:
                    #we've finished
                    if verbose: print("****finished?")
                    break

    else:

        grid_shapes=np.array([[6, 3 ,3 ,3 ,3 ,4],
                [6, 3, 2, 2, 2, 4],
                [6, 7, 2, 2, 1, 4],
                [6, 7, 7 ,1 ,1 ,4],
                [6, 7, 7, 1, 1, 9]])


        grid_shapes2=   np.array( [[ 3,  3,  3,  6,  6,  6],
                    [ 3,  4,  2,  2,  2,  6],
         [ 3,  4,  4,  2,  2,  6],
         [ 4,  4, 10,  1,  1,  1],
         [ 8,  8,  8,  8,  1,  1]])



    if verbose: print(grid_shapes)
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



    iterate_cell_count=0
    iterate_number_count=0
    start_time=time.time()


    #to save time with a large recursive function, use some additional data lookups

    iter_shapes={} #not working yet!!
    iter_nonshape_neighbours={}
    row_col={}
    for i in range(num_cols*num_rows):
        r = i // num_cols
        c = i % num_cols
        row_col[i]=(r,c)
        shape_no=grid_shapes[r,c]
        shapes = shape_coords[shape_no]
        max_nums = len(shapes)
        iter_shapes[i]=(max_nums,shapes)
        neighbours=get_neighbours(r,c)
        for nb in neighbours:
                if nb in shapes:
                    neighbours.remove(nb)


        iter_nonshape_neighbours[i]=neighbours


    def recurse(cell_iter_no):
        global iterate_number_count,iterate_cell_count, max_iters
        success=False
        rc=row_col[cell_iter_no]
        #r=cell_iter_no//num_cols
        #c=cell_iter_no%num_cols

        max_nums,shapes=iter_shapes[cell_iter_no]
        # shape_no=grid_shapes[(r,c)]
        # shapes=shape_coords[shape_no]
        # max_nums=len(shapes)

        nums_avail=list(range(1,max_nums+1))
        for shape in shapes:
            this_num=grid[shape]
            if this_num in nums_avail:
                nums_avail.remove(this_num)


        for num_to_try in nums_avail:
            grid[rc]=num_to_try
            iterate_number_count+=1
            #if iterate_number_count%500==0:
            #    display_newnumber("@",(r,c),"white")
            #    display_newnumber(num_to_try,(r,c))
            #print ("#",cell_iter_no,"rc",r,c,"num",num_to_try)

            #now let's check if valid
            valid=True
            # for shape in shapes:
            #     if shape!=(r,c) and grid[shape]==num_to_try:
            #         valid=False
            neighbours=iter_nonshape_neighbours[cell_iter_no]
            for nb in neighbours:
                if grid[nb]==num_to_try:
                    valid=False
                    break

            #if ok
            if valid:
                if cell_iter_no<num_rows*num_cols-1 and iterate_cell_count<max_iters:
                    iterate_cell_count+=1

                    if verbose:
                        if iterate_cell_count%10000==0:
                            elapsed=time.time()-start_time
                            if not elapsed:
                                rate=0
                            else:
                                rate=iterate_cell_count/elapsed
                            print (f"iterate counts {iterate_cell_count:,}",'{:,}'.format(iterate_number_count), "time",elapsed, "rate",rate)
                            #f"{num:,}"
                    result=recurse(cell_iter_no + 1)
                    if result:
                        success=True
                        break
                    else:

                        success=False #keep trying numbers

                else:
                    # we've actually completed
                    success=True


                    break

            #otherwise go up a number in for loop
            grid[rc] = 0
            #display_newnumber(num_to_try, (r, c),"white")

        if not success:
            #run out of numbers in this cell
            grid[rc]=0



        #print(grid)
        return(success)


    def real_iterate():
        global iterate_number_count,iterate_cell_count, max_iters
        success=False
        numbers_to_try_stack={}
        cell_iter_no = 0
        keep_iterating=True
        next_step="starting"
        while keep_iterating:
            #let's start loop off
            #print("next step",next_step)
            if next_step=="ascend":
                if cell_iter_no<num_rows*num_cols-1: #TODO create variable
                    cell_iter_no+=1
                    iterate_cell_count += 1
                    if verbose:
                        if iterate_cell_count % 50000 == 0:
                            elapsed = time.time() - start_time
                            if not elapsed:
                                rate = 0
                            else:
                                rate = iterate_cell_count / elapsed
                            print("iterate counts", iterate_cell_count, iterate_number_count, "cell", cell_iter_no,"time", elapsed, "rate", rate)
                else:
                    #got as far as end cell - complete
                    print ("*complete*")
                    success=True
                    break

            if next_step=="descend":
                grid[rc]=0
                cell_iter_no-=1
                if cell_iter_no<0:
                    next_step="FAIL"
                    break

            rc = row_col[cell_iter_no]
            #print ("rc",rc)

            if next_step=="ascend" or next_step=="starting":
                max_nums,shapes=iter_shapes[cell_iter_no]
                nums_avail=list(range(1,max_nums+1))
                for shape in shapes:
                    this_num=grid[shape]
                    if this_num in nums_avail:
                        nums_avail.remove(this_num)
                numbers_to_try_stack[cell_iter_no] = nums_avail

            elif next_step=="descend":
                max_nums, shapes = iter_shapes[cell_iter_no]  #TODO do we need shapes now?
                nums_avail = numbers_to_try_stack[cell_iter_no]

            #now we actually iterate do we?
            #print ("where we're at",cell_iter_no,nums_avail)

            if not nums_avail:
                #run out of numbers for cell, retreat
                next_step="descend"
            else:
                num_to_try = nums_avail.pop(0)
                numbers_to_try_stack[cell_iter_no] = nums_avail

                grid[rc]=num_to_try
                iterate_number_count+=1
                #now let's check if valid
                valid=True
                neighbours=iter_nonshape_neighbours[cell_iter_no]
                for nb in neighbours:
                    if grid[nb]==num_to_try:
                        valid=False
                        break

                #if ok - ascend a level in iteration
                if valid:
                    if cell_iter_no<num_rows*num_cols-1 and iterate_cell_count<max_iters:
                        iterate_cell_count+=1
                        next_step="ascend"
                        if iterate_cell_count%10000==0:
                            elapsed=time.time()-start_time
                            if not elapsed:
                                rate=0
                            else:
                                rate=iterate_cell_count/elapsed
                            print ("iterate counts",iterate_cell_count,iterate_number_count, "time",elapsed, "rate",rate)

                else:
                    #doesn't work try next number
                    next_step="inc_number"
                    grid[rc] = 0


            #this is end of while loop I think


        #print(grid)
        #END OF ITERATION
        return(success)






    success=real_iterate()
    if iterate_cell_count>=max_iters: success=False

    if success:
        print ("success?",success)
        print (grid)
        print (grid_shapes)

    elapsed = time.time() - start_time
    if elapsed>0:
        end_rate=iterate_cell_count / elapsed
    else:
        end_rate=0

    if True: #verbose:
        print (f"tries: {grids_tried}  iterate counts",iterate_cell_count,iterate_number_count,"time", elapsed, "rate", end_rate)

    # now numbers
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
            pen.forward(cell_draw_size)
        pen.right(90)
        pen.forward(cell_draw_size)
        pen.left(90)
        pen.backward(row_width + cell_draw_size)

    screen.tracer(0)




    grids_tried+=1
    if success or grids_tried>0:
        found_one_yet=success   #True to stop

print ("total grids tried",grids_tried)




turtle.done()

