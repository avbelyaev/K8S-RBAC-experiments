#! /usr/bin/env python3.6
import json

from functools import partial
from flask import Flask, jsonify
from flask import request

from backend.datasource import DataSource

print = partial(print, flush=True)

app = Flask(__name__)


@app.route('/api/docs', methods=['POST'])
def save_any():
    data = None
    req_json = request.get_json()
    if req_json is not None:
        data = req_json

    elif request.data is not None:
        # check if body is byte array and try converting to json
        req_bytes = request.data
        bytes_str = req_bytes.decode('utf8').replace('\'', '\\"')
        try:
            data = json.loads(bytes_str)
        except json.decoder.JSONDecodeError as e:
            print('error occurred while serializing data. saving as string!', e)
            return jsonify({'error': str(e)}), 400

    else:
        return jsonify({'info': 'nothing to save'}), 200

    print(f'Saving data')
    DataSource(app).save_one(data)
    return jsonify({'info': 'request has been saved!'}), 200


@app.route("/api/docs", methods=['GET'])
def get_all():
    print('Listing data')
    items = DataSource(app).find_all()
    return jsonify({'items': items}), 200


@app.route("/api/headers")
def headers():
    rq_headers = dict(request.headers.items())
    return jsonify({'headers': rq_headers}), 200


@app.route("/api/hello")
def hello():
    return jsonify({'info': 'Hello flask 2!'}), 200


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


# apparently the only way to handle /**
@app.route('/', defaults={'u_path': ''})
@app.route('/<path:u_path>')
def catch_all(u_path):
    print(repr(u_path))


# after we have patched app with controllers, we can return it's 'final form'
def get_app() -> Flask:
    return app


if __name__ == '__main__':
    print(f'starting from app.py')

    print(app.url_map)
    app.run(host='0.0.0.0', port=5000)  # to be able to run in container
