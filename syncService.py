from dataSync import DAU
import os
from pymongo import MongoClient
from bson.json_util import dumps
import pusher

MONGO_URL = os.getenv('MONGO_URL')
MONGO_DRS_URL = os.getenv('MONGO_DRS_URL')

client = MongoClient(os.environ['MONGO_URL'])
pusher_client = pusher.Pusher(app_id=u'1132712', key=u'84b1efe772a7e8d6f44b', secret=u'1ef976f8eb09f3bfbd63', cluster=u'ap2')

print('Listing for changes in Users collection..')
change_stream = client.iDreamCareer.users.watch([
      { "$match" : {"operationType" : "insert" } }
   ])

for change in change_stream:
    print(dumps(change))
    print('') # for readability only
    DAU()
    pusher_client.trigger(u'idc2-production', u'dau_update_event', {u'dau_update': u'true'})

# DAU()
# pusher_client.trigger(u'idc2-production', u'dau_update_event', {u'dau_update': u'true'})
