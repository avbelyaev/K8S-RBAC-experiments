#! /usr/bin/env python3.6
import os
from flask import Flask
from flask import request
from flask_pymongo import PyMongo
from functools import partial
from bson.json_util import dumps

print = partial(print, flush=True)

MONGO_HOST = os.environ.get('MONGO_HOST') if os.environ.get('MONGO_HOST') is not None else 'localhost'
MONGO_PORT = 27017
MONGO_DB = 'kube'

app = Flask(__name__)
app.config['MONGO_URI'] = f'mongodb://admin:admin@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}'
mongo = PyMongo(app)

#
# @app.route('/users/<email>', methods=['POST'])
# def save_user(email):
#     print(f'Attempting to save user with email {email}')
#
#     users = User.objects
#     existing_user = next(filter(lambda user_doc: user_doc.email == email, users), None)
#     if existing_user:
#         print(f'User with email {email} already exists')
#         return app.response_class(
#             response=json.dumps({'msg': 'user already exists'}),
#             status=409,
#             mimetype='application/json'
#         )
#
#     else:
#         user = User()
#         user.email = email
#         user.save()
#         print(f'User with email {email} has been successfully saved')
#         return app.response_class(
#             response=json.dumps({'msg': f'User {email} has been saved!\n'}),
#             status=200,
#             mimetype='application/json'
#         )


@app.route('/any', methods=['POST'])
def save_any():
    data = request.get_json()
    print(f'Saving {data}')

    mongo.db.kube.insert_one(data)
    return app.response_class(
        response=dumps({'msg': f'request body has been saved!\n'}),
        status=200,
        mimetype='application/json'
    )


@app.route("/all", methods=['GET'])
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


@app.route("/headers")
def headers():
    rq_headers = request.headers
    return f'Headers from rq:\n{rq_headers}'


@app.route("/hello")
def hello():
    return "Hello Flask v2!\n"


if __name__ == '__main__':
    print(f'Connecting to mongo at {MONGO_HOST}:{MONGO_PORT}')
    app.run(host='0.0.0.0', port=5000)  # to be able to run in container
