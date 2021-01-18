from dataSync import DAU
import os
from pymongo import MongoClient
from bson.json_util import dumps

MONGO_URL = os.getenv('MONGO_URL')
MONGO_DRS_URL = os.getenv('MONGO_DRS_URL')

client = MongoClient(os.environ['MONGO_URL'])

print('Listing for changes in Users collection..')
change_stream = client.iDreamCareer.users.watch([
      { "$match" : {"operationType" : "insert" } }
   ])

for change in change_stream:
    print(dumps(change))
    print('') # for readability only
    DAU()

# DAU()