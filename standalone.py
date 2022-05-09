import gridgenerate as gridgen
import database_functions as db
from time import time


def findandsolvegrids():
    ######JUST STARTING THIS
    #find multiple grids from database and try solving
    #global initial variables
    gridgen.num_rows=5   #probably not the way we want to keep that going
    gridgen.num_cols=7
    gridgen.verbose=False
    gridgen.display_build=False

    start_time=time()
    # num_success=0
    # num_timeout=0
    number_to_loop=1 #11 is good for getting up to 10x12
    for loop in range(number_to_loop):
        #need to find from database

        gridgen.create_blank_grids()
        gridgen.gen_predet_shapes(turtle_fill=False)

        # gridgen.shape_coords = gridgen.get_shape_coords()
        # gridgen.max_iters = 1e6
        # gridgen.iterate_cell_count = 0
        # gridgen.iterate_number_count = 0
        #
        # gridgen.create_iterate_lookups()
        # success = gridgen.real_iterate()
        # #TODO refactor so success is yes/no/timeout
        # if gridgen.iterate_cell_count>=gridgen.max_iters:
        #     num_timeout+=1
        # else:
        #     if success:
        #         num_success+=1

        elapsed= round(time()-start_time,2)
        print (f"grid size {gridgen.num_rows},{gridgen.num_cols}   elapsed {elapsed}")
        print (gridgen.grid_shapes)

        #now save to database
        doc_name = f"{gridgen.num_rows},{gridgen.num_cols}"  #name is dimensions
        to_upsert = {"record_type":"for_time_trial", "rows":gridgen.num_rows, "cols":gridgen.num_cols,
                     "generator_type":"standard predef shapes",
                    "grid_shapes": gridgen.grid_shapes.tolist()}
        db.upsert({"name": doc_name}, to_upsert)



        if loop%2==0:
            gridgen.num_rows+=1
        else:
            gridgen.num_cols+=1

def genandsavegrids():
    #generate and save  multiple grids
    #global initial variables
    gridgen.num_rows=5
    gridgen.num_cols=7
    gridgen.verbose=False
    gridgen.display_build=False

    start_time=time()
    # num_success=0
    # num_timeout=0
    number_to_loop=11 #11 is good for getting up to 10x12
    for loop in range(number_to_loop):
        gridgen.create_blank_grids()
        gridgen.gen_predet_shapes(turtle_fill=False)

        # gridgen.shape_coords = gridgen.get_shape_coords()
        # gridgen.max_iters = 1e6
        # gridgen.iterate_cell_count = 0
        # gridgen.iterate_number_count = 0
        #
        # gridgen.create_iterate_lookups()
        # success = gridgen.real_iterate()
        # #TODO refactor so success is yes/no/timeout
        # if gridgen.iterate_cell_count>=gridgen.max_iters:
        #     num_timeout+=1
        # else:
        #     if success:
        #         num_success+=1

        elapsed= round(time()-start_time,2)
        print (f"grid size {gridgen.num_rows},{gridgen.num_cols}   elapsed {elapsed}")
        print (gridgen.grid_shapes)

        #now save to database
        doc_name = f"{gridgen.num_rows},{gridgen.num_cols}"  #name is dimensions
        to_upsert = {"record_type":"for_time_trial", "rows":gridgen.num_rows, "cols":gridgen.num_cols,
                     "generator_type":"standard predef shapes",
                    "grid_shapes": gridgen.grid_shapes.tolist()}
        db.upsert({"name": doc_name}, to_upsert)



        if loop%2==0:
            gridgen.num_rows+=1
        else:
            gridgen.num_cols+=1




if __name__ == '__main__':
    db.connect_suguru_db()
    #genandsavegrids()  'do just once usually
