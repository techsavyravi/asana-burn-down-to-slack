from dataSync import DAU
import os
from pymongo import MongoClient
from bson.json_util import dumps

MONGO_URL = os.getenv('MONGO_URL')

DAU(2)