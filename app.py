# -*- coding: utf-8 -*-
from flask import Flask, request, render_template, jsonify
from flask_sentinel import ResourceOwnerPasswordCredentials, oauth
import utils.SchemaValidator as schema
import json
from user.route_me import route_me
from werkzeug.routing import BaseConverter
from utils.TokenBearer import InvalidUsage

app = Flask(__name__)

from storage import models

class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

app.url_map.converters['regex'] = RegexConverter

app.register_blueprint(route_me)

ResourceOwnerPasswordCredentials(app)
app.config['DEBUG'] = True

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response                = jsonify(error.to_dict())
    response.status_code    = error.status_code
    return response

@app.route('/<regex("[a-z]{4,10}"):seed>-<slug>/<regex("[a-z, 0-9]{2,20}"):woof>')
def example(seed, slug, woof):
    return "seed: %s" % seed, woof

@app.route('/')
def home():
    return render_template('doc.html', url_root=request.url_root)

if __name__ == '__main__':
    app.run(ssl_context='adhoc')
