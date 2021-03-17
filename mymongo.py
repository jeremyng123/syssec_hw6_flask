from pymongo import MongoClient
from bson.objectid import ObjectId
from constants import *

global db


def getMongoDBClient():
    return MongoClient()[MONGODB_NAME]


def getMongoDBCollection(this, collectionName):
    try:
        return this[collectionName]
    except:
        print("db not init yet")


if __name__ == "__main__":
    db = getMongoDBClient()
    print(getMongoDBCollection('user').find_one())
