# -*- coding: utf-8 -*-
'''
Database Functions
These will be shared across different entry points (web, own computer etc)
Created on 6 MAY 2022!!
@author: Ashley Malster
'''

import os
from pymongo import MongoClient

def connect_suguru_db():
    #global my_db_collection
    ## CONNECT TO MONGO_DB
    # use environment variable rather than hard code secrets - but format is along lines of:
    # conn_str = "mongodb+srv://<username>:<password>@<cluster-address>/test?retryWrites=true&w=majority"
    connection_string = os.environ.get("SUGURU_CONN_STR")
    myclient = MongoClient(connection_string)
    mydb = myclient['suguru']
    my_db_collection = mydb['suguru_test']
    return my_db_collection


##to access/read one document
#gamedata=mycollection.find_one({"GameID":GameID})

##to write one document (either update or insert/create -- so upsert)
#to_upsert={"$set":{"restart_next":False}}
#result=mycollection.update_one({"GameID":GameID},to_upsert,upsert=True)

