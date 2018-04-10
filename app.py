# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, url_for
from flask_sentinel import ResourceOwnerPasswordCredentials
from user.route_me import route_me
from utils.TokenBearer import InvalidUsage
from pet.route_woof import route

app = Flask(__name__)
app.config['DEBUG'] = True
#app.config['SENTINEL_MONGO_HOST'] = "mongodb://kaka"
app.config['SENTINEL_MONGO_URI'] = "mongodb://mongodb"
app.config['SENTINEL_REDIS_URL'] = "redis://redisdb:6379/0"
from storage import models

route(app)
app.register_blueprint(route_me)

ResourceOwnerPasswordCredentials(app)


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response                = jsonify(error.to_dict())
    response.status_code    = error.status_code
    return response

@app.route('/')
def home():
    return render_template('doc.html', url_root= url_for('home', _external=True))

if __name__ == '__main__':
    app.run(ssl_context='adhoc')
