#! /usr/bin/env python3.6
import json
import os

from bson.json_util import dumps
from flask import Flask
from flask import request
from flask_pymongo import PyMongo
from functools import partial

print = partial(print, flush=True)

MONGO_HOST = os.environ.get('MONGO_HOST') if os.environ.get('MONGO_HOST') is not None else 'localhost'
MONGO_PORT = 27017
MONGO_DB = 'kube'

app = Flask(__name__)
app.config['MONGO_URI'] = f'mongodb://admin:admin@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}'
mongo = PyMongo(app)


@app.route('/api/docs', methods=['POST'])
def save_any():
    data = None
    req_json = request.get_json()
    if req_json is not None:
        data = req_json

    elif request.data is not None:
        # check if body is byte array and convert to json
        req_bytes = request.data
        bytes_str = req_bytes.decode('utf8').replace('\'', '\\"')
        try:
            data = json.loads(bytes_str)
        except json.decoder.JSONDecodeError as e:
            data = {
                'data': bytes_str,
                'error': str(e)
            }

    else:
        return app.response_class(
            response=dumps({'msg': 'nothing to save'}),
            status=200,
            mimetype='application/json'
        )

    print(f'Saving data')
    mongo.db.kube.insert_one(data)
    return app.response_class(
        response=dumps({'msg': 'request has been saved!'}),
        status=200,
        mimetype='application/json'
    )


@app.route("/api/docs", methods=['GET'])
def get_all():
    print('Listing data')
    objects = []
    items = mongo.db.kube.find({})
    for item in items:
        objects.append(item)

    return app.response_class(
        response=dumps({'items': objects}),
        status=200,
        mimetype='application/json'
    )


@app.route("/api/headers")
def headers():
    rq_headers = request.headers
    return app.response_class(
        response=dumps(rq_headers),
        status=200,
        mimetype='application/json'
    )


@app.route("/api/hello")
def hello():
    return app.response_class(
        response=dumps({'msg': 'Hello flask!'}),
        status=200,
        mimetype='application/json'
    )


if __name__ == '__main__':
    print(f'Connecting to mongo at {MONGO_HOST}:{MONGO_PORT}')
    app.run(host='0.0.0.0', port=5000)  # to be able to run in container
