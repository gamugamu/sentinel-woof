# -*- coding: utf-8 -*-
from flask import Flask, request, render_template
from flask_sentinel import ResourceOwnerPasswordCredentials, oauth
import utils.SchemaValidator as schema
import json
from user.profil import profil
from werkzeug.routing import BaseConverter

app = Flask(__name__)

from storage import models

class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

app.url_map.converters['regex'] = RegexConverter

app.register_blueprint(profil)

ResourceOwnerPasswordCredentials(app)
app.config['DEBUG'] = True

@app.route('/<regex("[a-z]{4,10}"):seed>-<slug>/<regex("[a-z, 0-9]{2,20}"):woof>')
def example(seed, slug, woof):
    return "seed: %s" % seed, woof

@app.route('/')
def home():
    return render_template('doc.html', url_root=request.url_root)


if __name__ == '__main__':
    app.run(ssl_context='adhoc')
