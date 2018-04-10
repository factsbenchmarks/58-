import pymongo
import time
client = pymongo.MongoClient('localhost',27017)
db = client['58city']
col = db['detail_info']
while True:
    print(col.find().count())
    time.sleep(5)

