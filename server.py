from sanic import Sanic
from sanic.response import text
import pymongo

import config

app = Sanic("MyHelloWorldApp")


class DatabaseController():
    mongo = None

    def __init__(self):
        client = pymongo.MongoClient(
            host=config.MONGODB_HOST,
            port=config.MONGODB_PORT, 
            username=config.MONGODB_USERNAME, 
            password=config.MONGODB_PASSWORD, 
            authSource="admin",
        )  
        # Create the database for our example (we will use the same database throughout the tutorial
        self.mongo = client[config.MONGODB_DATABASE]

DB = None

@app.listener('before_server_start')
def serverStart(app, loop):
    DB = DatabaseController()

@app.get("/")
async def hello_world(request):
    return text("Hello, world.")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, fast=True) 