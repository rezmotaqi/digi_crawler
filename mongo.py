import os
import pymongo


try:
    mongo_uri = 'mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ['MONGODB_PASSWORD'] + '@' + os.environ[
        'MONGODB_HOSTNAME'] + ':27017/' + os.environ['MONGODB_DATABASE']
except (ValueError, KeyError):
    mongo_uri = "mongodb://localhost:27017/"


myclient = pymongo.MongoClient(mongo_uri)

mydb = myclient["digi"]
products_collection = mydb["products"]
product_history_collection = mydb["products_history"]
