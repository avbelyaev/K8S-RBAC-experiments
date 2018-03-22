#! /usr/bin/env python3.6
# @author anton.belyaev@bostongene.com
import os
from flask import Flask
from flask_mongoengine import MongoEngine, Document
from mongoengine import StringField


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


@app.route("/")
def hello():
    return "Hello Flask!"


@app.route('/users/<email>', methods=['POST'])
def save_user(email):
    print(f'Attempting to save user with email {email}', flush=True)

    existing_user = next(filter(lambda user_doc: user_doc.email == email, User.objects), None)
    if existing_user:
        print(f'User with email {email} already exists', flush=True)
        return 'Ignored as duplicate\n'

    else:
        user = User()
        user.email = email
        user.save()
        print(f'User with email {email} successfully saved')
        return f'User {email} has been saved!\n'


@app.route("/users")
def list_users():
    print('Listing users', flush=True)
    users = User.objects
    return '\n'.join(map(lambda user: user.email, users)) if users else 'User list is empty'


if __name__ == '__main__':
    db.init_app(app)
    app.run(host='0.0.0.0')
