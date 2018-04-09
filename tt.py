import pymongo
client = pymongo.MongoClient('localhost',27017)
db = client['58']
col = db['house58']
for i in col.find({'price':{'$lt':2000}}):
    print(i)

# for i in col.find():
#     if i['price']<1000:
#         print(i)
