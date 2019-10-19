import os

from bson.json_util import dumps
from flask_pymongo import PyMongo

mongo = None


class DataStore:
    def __init__(self, app):
        self.app = app

    def _get_mongo(self) -> PyMongo:
        global mongo
        if mongo:
            return mongo

        mongo_host = 'localhost'
        if os.environ.get('MONGO_HOST'):
            mongo_host = os.environ.get('MONGO_HOST')
        mongo_port = 27017
        mongo_db = 'kube'
        print(f'connecting to mongo at {mongo_host}:{mongo_port}/{mongo_db}')

        self.app.config['MONGO_URI'] = f'mongodb://admin:admin@{mongo_host}:{mongo_port}/{mongo_db}'
        mongo = PyMongo(self.app)
        return mongo

    def save_one(self, item):
        self._get_mongo().db.kube.insert_one(item)

    def find_all(self) -> list:
        items = []
        items_found = self._get_mongo().db.kube.find({})
        for item in items_found:
            transformed_item = item
            # ObjectId is not serializable.
            # this hack replaces not-serializable field with str(ObjectId)
            transformed_item['_id'] = str(item['_id'])
            items.append(item)
        return items
