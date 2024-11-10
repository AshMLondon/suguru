#Puzzle Analysis
#create some puzzle grids and analyse what they contain

from puzzle import Puzzle
import random, time, json
import sys
from collections import defaultdict


def generate_results(count=False):

    print(sys.version)
    scores = defaultdict(int)
    overall_start_time = time.time()
    filename="data_output/puzzle_analysis_results.json"
    description={"description":f"puzzle analysis {sys.version}"}
    total_iters=0
    if not count:
        count=20

    results=[]
    success_to_save=[]



    for n in range(count):
        print()
        print("**PUZZLE SETUP**")
        puzzle = Puzzle(7, 8)
        random.seed(100 + n)
        puzzle.generate_grid_shapes()
        puzzle.generate_iteration_lookups()
        puzzle.smaller_surrounded_check_all()
        #print("----SOLVING---")
        start_time = time.time()
        success = puzzle.better_solver(multi=False)
        result_to_print = "none"
        if success:
            result_to_print = "SOLUTION"
        elif puzzle.iteration_timeout:
            result_to_print = "timeout"
        scores[result_to_print] += 1

        if not puzzle.iteration_timeout:
            total_iters+=puzzle.iteration_counter

        print(f"#{n} {result_to_print} {puzzle.iteration_counter} {time.time() - start_time}")
        print("VALIDITY CHECK",puzzle.is_whole_thing_valid())
        this_result={
            "number":n, "result":result_to_print, "time":time.time()-start_time,
            "shapes":puzzle.shapes, "shape_cells":puzzle.shape_cells
        }
        results.append(this_result)

        if success:
            success_to_save.append({"shapes":puzzle.shapes,"solution":puzzle.solution,"givens":puzzle.givens})

    filename1=f"grids_{puzzle.rows}x{puzzle.cols}"
    with open(filename1, "a") as file:
        json.dump(success_to_save,file,indent=2)





    print(scores)
    print("total time", time.time() - overall_start_time)
    print(scores["SOLUTION"]/count*100,"%")
    print ("total iterations (success+fail, not timeout)",total_iters)




    output={"description":description, "results":results}

    with open(filename, 'w') as file:
        json.dump(output,file,indent=2)
        #json.dump(description,file,indent=2)


def analyse_results():
    filename="data_output/puzzle_analysis_results.json"
    with open(filename, 'r') as file:
        inputdict = json.load(file)

    with open("shape_permutations.json", 'r') as f:
        standard_shapes = json.load(f)

    # print ("IPD",inputdict)
    description=inputdict["description"]
    results=inputdict["results"]
    #results should be a list of individual grid generation results - number, time, succesful, and the grid
    fail_scores=defaultdict(int)
    success_scores=defaultdict(int)
    duration=0
    max_shapes=0
    min_shapes=1e99
    for result in results:
        outcome=result["result"]
        shape_cells=result["shape_cells"]
        duration+=result["time"]
        num_shapes=len(shape_cells)
        max_shapes=max(max_shapes,num_shapes)
        min_shapes=min(min_shapes,num_shapes)

        match_count=0
        for shape in shape_cells.values():
            shape=rebase(shape)
            #now check which standard shape this represents
            #print(standard_shapes)
            for std_shape_entry  in standard_shapes:
                std_shape_name=std_shape_entry[0]
                std_shape_cells=std_shape_entry[1]
                if shape in std_shape_cells:
                    #print(std_shape_name)
                    match_count+=1
                    if outcome=="SOLUTION":
                        success_scores[std_shape_name] += 1

                    elif outcome=="none":
                        fail_scores[std_shape_name]+=1
                    break

    #print("count",match_count)
    fail_total=0
    for score in fail_scores.values():
       fail_total+=score
    print("FAIL",fail_total,fail_scores)

    success_total = 0
    for score in success_scores.values():
        success_total += score
    print("SOL", success_total,success_scores)

    #now compare percentages
    comparison=[]
    for shape in fail_scores:
        fail_percent=fail_scores[shape]/fail_total*100
        success_percent=success_scores.get(shape,0)/success_total*100
        comparison.append([round(success_percent-fail_percent,1),shape])


    print(description)
    print("TOTAL RESULTS ANALYSED",len(results))
    print("total time needed  to generate grids ",round(duration/60,1),"minutes")
    print("success % ",)
    print (f"MAX {max_shapes} MIN {min_shapes} shapes per grid")
    comparison.sort()
    print("DELTA",comparison)




def rebase(shape):
    #rebase=convert shape into a set of cells starting at 0,0 in ascending order
    shape.sort()
    start_r,start_c=shape[0]
    newshape=[]
    for cell in shape:
        newshape.append([cell[0]-start_r,cell[1]-start_c])
    return newshape



if __name__ == '__main__':
    print (sys.version)
    generate_results(50)
    #analyse_results()


    quit()
    temp_shape_dict={'corner-3': 3638, 'T-4': 5279, 'L-4': 5794, 'snake': 5175, 'gun': 6780, 'line-4': 2537, 'T': 3917, 'S': 3357, 'line-2': 8342, 'snail': 11501, 'steps': 4938, 'line-3': 3303, 'line-5': 5874, 'box-4': 2672, 'cross': 1938, 'L': 8974, 'snake-4': 1772, 'seahorse': 3943, 'cell-1': 908}
    ordering=[]
    for name,score in temp_shape_dict.items():
        ordering.append([score,name])
    ordering.sort()
    print(ordering)
