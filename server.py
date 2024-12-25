from sanic import Sanic
from sanic import response
import pymongo
import json
from bson.objectid import ObjectId
from datetime import datetime

import config

app = Sanic("ToTheMoon")


class DB:
    mongo:pymongo.MongoClient = None

    @staticmethod
    def init():
        DB.mongo = DB.connectMongo()

    @staticmethod
    def connectMongo():
        client = pymongo.MongoClient(
            host=config.MONGODB_HOST,
            port=config.MONGODB_PORT, 
            username=config.MONGODB_USERNAME, 
            password=config.MONGODB_PASSWORD, 
            authSource="admin",
        )  
        print("-- Connected to MongoDB")
        return client[config.MONGODB_DATABASE]

# Ensure the result can be serialized by JSONEncoder
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)  # convert ObjectId to string
        elif isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')  # convert datetime to string
        return super().default(obj)

# Run something before the starting of server
@app.listener('before_server_start')
def serverStart(app, loop):
    DB.init()

@app.get("/")
async def hello_world(request):
    return response.text("Hello, world.")

@app.route("/getServices", methods=['GET'])
async def getServices(request):
    services = list(DB.mongo["services"].find())
    return response.text(json.dumps(services, cls=CustomJSONEncoder), content_type='application/json', status=200)

@app.route("/setService", methods=['GET'])
async def setService(request):
    service = {
        "name": "Take wedding photos",
        "description": "test",
        "price": 100
    }
    DB.mongo["services"].insert_one(service)
    return response.text("success", content_type='application/json', status=200)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, fast=True) 