#! /usr/bin/env python3.6
# @author anton.belyaev@bostongene.com
from flask_sqlalchemy import SQLAlchemy

import g

g.db = SQLAlchemy()


class User(g.db.Model):
    __tablename__ = "users"
    id = g.db.Column(g.db.Integer, primary_key=True)
    email = g.db.Column(g.db.String(120), unique=True)

    def __init__(self, email):
        self.email = email

    def __repr__(self):
        return f'({self.__str__()})'

    def __str__(self):
        return f'User "{self.email}"'
