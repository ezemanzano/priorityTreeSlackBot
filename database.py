
from datetime import datetime, timedelta
import time
import os
from pymongo import MongoClient, DESCENDING, ASCENDING


# Connect to MongoDB database
mongo = MongoClient(os.getenv("MONGODB_CONNECTION"))
db = mongo[os.getenv("DB_NAME")]
collection = db[os.getenv("DB_COLLECTION")]

date = int((datetime.now() + timedelta(seconds=20)).timestamp())

# Define the functions for ABM commands
def add_item(item):
    collection.insert_one(item)
    return True

def delete_item(id):
    collection.delete_one({"id": int(id)})
    return True

def modify_item(id, new_order):
    collection.update_one({"id": int(id)}, {"$set": {'order' : int(new_order), 'modified': datetime.now().timestamp()}})

def list_items():
    items = []
    for item in collection.find().sort([('order', ASCENDING),('modified', DESCENDING)]):
        items.append({'name': str(item['name']),'order':str(item['order']), 'id' : str(item['id'])})
    return items


def last_order():
    if collection.count_documents({}) == 0:
        return 0
    else:
        result = collection.find().sort('order', DESCENDING).limit(1)
        return int(result[0]['order']) 


def last_id():
    if collection.count_documents({}) == 0:
        return 0
    else:
        result = collection.find().sort('id', DESCENDING).limit(1)
        return int(result[0]['id']) 
    
def getAmount():
    return collection.count_documents({})


def orderPriorityTree():
    if collection.count_documents({}) == 0:
        return None
    orden = 1
    for item in collection.find().sort([('order', ASCENDING),('modified', DESCENDING)]):
        modify_item(int(item['id']),orden)
        orden=orden+1


def editOrderPriorityTree(items):
    if collection.count_documents({}) == 0:
        return None
    orden = 1
    for item in items:
        modify_item(int(item),orden)
        orden=orden+1

def checkIfAllExist(items):
    for item in items:
        if collection.count_documents({'id' : int(item)}) == 0:
            return False
        return True
            