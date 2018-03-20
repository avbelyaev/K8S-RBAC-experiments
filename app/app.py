#! /usr/bin/env python3.6
# @author anton.belyaev@bostongene.com

from flask import Flask
app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"
