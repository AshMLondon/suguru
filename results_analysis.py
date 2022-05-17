##analyse existing results that are in the database
import database_functions as db
from pprint import pprint

my_collection = db.connect_suguru_db("solved_grids")
size_to_find="10x13"

results=my_collection.find() #({"size":size_to_find})

solveable_shapes=[]

for result in results:
    solveable_shapes.append(result["grid_shapes"])


print (len(solveable_shapes))

list2=[]
for element in solveable_shapes:

    tuple_res = tuple(tuple(sub) for sub in element)
    list2.append(tuple_res)

print (len((list2)))
print (len(set(list2)))

#pprint(solveable_shapes)




