#! /usr/bin/env python3.6
import json
import os
from flask import Flask
from flask_mongoengine import MongoEngine, Document
from flask import request
from mongoengine import StringField
from functools import partial

print = partial(print, flush=True)


MONGO_HOST = os.environ.get('MONGO_HOST') if os.environ.get('MONGO_HOST') is not None else 'localhost'
MONGO_PORT = 27017


class User(Document):
    email = StringField(required=True)


app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'kube',
    'host': MONGO_HOST,
    'port': MONGO_PORT,
    'username': 'admin',
    'password': 'admin'
}
db = MongoEngine()


@app.route('/users/<email>', methods=['POST'])
def save_user(email):
    print(f'Attempting to save user with email {email}')

    users = User.objects
    existing_user = next(filter(lambda user_doc: user_doc.email == email, users), None)
    if existing_user:
        print(f'User with email {email} already exists')
        return app.response_class(
            response=json.dumps({'msg': 'user already exists'}),
            status=409,
            mimetype='application/json'
        )

    else:
        user = User()
        user.email = email
        user.save()
        print(f'User with email {email} has been successfully saved')
        return app.response_class(
            response=json.dumps({'msg': f'User {email} has been saved!\n'}),
            status=200,
            mimetype='application/json'
        )


@app.route("/users")
def list_users():
    print('Listing users')
    users = User.objects
    return app.response_class(
        response=json.dumps(users),
        status=200,
        mimetype='application/json'
    )


@app.route("/headers")
def headers():
    rq_headers = request.headers
    return app.response_class(
        response=json.dumps(rq_headers),
        status=200,
        mimetype='application/json'
    )


@app.route("/hello")
def hello():
    return "Hello Flask v2!\n"


if __name__ == '__main__':
    print(f'Connecting to mongo at {MONGO_HOST}:{MONGO_PORT}')
    db.init_app(app)
    app.run(host='0.0.0.0')     # to be able to run in container
