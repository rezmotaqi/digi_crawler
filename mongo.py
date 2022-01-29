import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["digi"]
products_collection = mydb["products"]