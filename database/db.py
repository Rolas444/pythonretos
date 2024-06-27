from dotenv import load_dotenv
import os
from pymongo import MongoClient

load_dotenv()
stringconnection = os.getenv('MONGO_URI')

def get_db():
    clientemongo = MongoClient(stringconnection)
    return clientemongo.pythonapp