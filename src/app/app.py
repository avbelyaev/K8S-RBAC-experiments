#! /usr/bin/env python3.6
# @author anton.belyaev@bostongene.com
import os
from flask import Flask
import g
from models import User

DB_USER = 'root'
DB_PWD = 'root'
DB_HOST = os.environ['DB_HOST']
DB_PORT = 5432
DB_NAME = 'mydb'


g.app = Flask(__name__)
g.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
g.app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PWD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'


@g.app.route("/")
def hello():
    return "Hello Flask!"


@g.app.route('/add/<email>', methods=['POST'])
def save_user(email):
    print(f'Saving user {email}', flush=True)
    if not g.db.session.query(User).filter(User.email == email).count():
        user = User(email)
        g.db.session.add(user)
        g.db.session.commit()
        return f'User with email {email} has been saved!'

    else:
        return 'Duplicate ignored'


@g.app.route("/list")
def list_users():
    print('Listing users', flush=True)
    all_entries = g.db.session.query(User).all()
    return '\n'.join(map(str, all_entries)) if all_entries else 'Empty list'


if __name__ == '__main__':
    g.db.init_app(g.app)
    with g.app.app_context():
        print('Creating tables', flush=True)
        g.db.create_all()
    g.app.run()
