#! /usr/bin/env python3.6
import os
from flask import Flask
from flask_mongoengine import MongoEngine, Document
from flask import request
from mongoengine import StringField
from functools import partial

print = partial(print, flush=True)


MONGO_HOST = os.environ['MONGO_HOST']
MONGO_PORT = int(os.environ['MONGO_PORT'])


class User(Document):
    email = StringField(required=True)


app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'users',
    'host': MONGO_HOST,
    'port': MONGO_PORT
}
db = MongoEngine()


@app.route('/users/<email>', methods=['POST'])
def save_user(email):
    print(f'Attempting to save user with email {email}')

    existing_user = next(filter(lambda user_doc: user_doc.email == email, User.objects), None)
    if existing_user:
        print(f'User with email {email} already exists')
        return 'Ignored as duplicate\n'

    else:
        user = User()
        user.email = email
        user.save()
        print(f'User with email {email} has been successfully saved')
        return f'User {email} has been saved!\n'


@app.route("/users")
def list_users():
    print('Listing users')

    users = User.objects
    if users:
        return '\n'.join(map(lambda user: user.email, users))

    else:
        return 'User list is empty\n'


@app.route("/headers")
def headers():
    rq_headers = request.headers
    return f'Headers:{rq_headers}'


@app.route("/hello")
def hello():
    return "Hello Flask v2!\n"


if __name__ == '__main__':
    print(f'Connecting to mongo at {MONGO_HOST}:{MONGO_PORT}')
    db.init_app(app)
    app.run(host='0.0.0.0')
