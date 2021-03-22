# Small utils for mongo db
from pymongo import MongoClient


def checkUserInDatabase(self):
    return True


def initMongoFromCloud(cloud):
    if cloud == 'supply':
        return MongoClient('localhost:27017',
                           username="developer",
                           password="team22_developer",
                           authSource="team22_supply")
    elif cloud == 'demand':
        return MongoClient('localhost:27017',
                           username="developer",
                           password="team22_developer",
                           authSource="team22_demand")
