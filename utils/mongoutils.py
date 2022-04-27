# Small utils for mongo db
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

mongo_secret = os.getenv("MONGO_SECRET")

def checkUserInDatabase(self):
    return True


def initMongo():
    return MongoClient('localhost:27017',
                       username="wego-deploy",
                       password=f"{mongo_secret}",
                       authSource=f"wego-db")
