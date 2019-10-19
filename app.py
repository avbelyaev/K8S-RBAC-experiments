#! /usr/bin/env python3.6
import json
import os

from functools import partial
from bson.json_util import dumps
from flask import Flask
from flask import request
from flask_pymongo import PyMongo

# to write into container stdout directly not waiting for buffer flush
print = partial(print, flush=True)


def create_app() -> Flask:
    app = Flask(__name__)
    return app


def init_mongo(app: Flask) -> PyMongo:
    mongo_host = 'localhost'
    if os.environ.get('MONGO_HOST'):
        mongo_host = os.environ.get('MONGO_HOST')
    mongo_port = 27017
    mongo_db = 'kube'
    print(f'connecting to mongo at {mongo_host}:{mongo_port}/{mongo_db}')

    app.config['MONGO_URI'] = f'mongodb://admin:admin@{mongo_host}:{mongo_port}/{mongo_db}'
    return PyMongo(app)


app = create_app()
mongo = init_mongo(app)


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


@app.route('/')
@app.route('/index')
def index():
    page_data = {
        'name': 'Flask!'
    }
    return '''
    <html>
      <head>
        <title>Home Page</title>
      </head>
      <body>
        <h1>Hello, ''' + page_data['name'] + '''</h1>
      </body>
    </html>
    '''


# for testing purpose:
# after we have patched app with controllers, we can return it's 'final form'
def get_app_for_test() -> Flask:
    return app


if __name__ == '__main__':
    print(app.url_map)
    app.run(host='0.0.0.0', port=5000)  # to be able to run in container
