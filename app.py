# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, url_for
from flask_sentinel import ResourceOwnerPasswordCredentials
from user.route_me import route_me
from utils.TokenBearer import InvalidUsage
from images_upload.uploader import bucket_setup
from pet.route_woof import route as pet_route
from test.route_test import route as test_route
from friends.route_friends import route as friends_route
from captcha_gen.capt import setup as capt_setup
from os import environ


app = Flask(__name__)
app.config['DEBUG'] = True

# depuis Docker, les urls localhost sont innaccessibles. Les links mongodb et redisdb
# ont été défini dans le ficher docker stack.yml. Ce qui veut dire
# que l'appli ne peut pas acceder à ces url hors docker. En externe, on veut
# réacceder à localhost de manière normal, donc on bypass cette configuration si hors Docker.
if environ.get('NUC') is not None:
    #TODO refactor
    app.config['SENTINEL_MONGO_URI'] = "mongodb://mongodb"
    app.config['SENTINEL_REDIS_URL'] = "redis://redisdb:6379/0"

from storage import models

pet_route(app)
test_route(app)
friends_route(app)
capt_setup(environ.get('NUC'))

#TODO refactor
app.register_blueprint(route_me)
ResourceOwnerPasswordCredentials(app)
# bucket
print "environ ",  environ.get('BUCKET_BASE_URL')
bucket_setup(base_url=environ.get('BUCKET_BASE_URL'))

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response                = jsonify(error.to_dict())
    response.status_code    = error.status_code
    return response

@app.route('/')
def home():
    from user.credential import internal_url
    #TODO refactor
    is_local_host = "localhost" in request.host_url or "0.0.0.0" in request.host_url
    return render_template('doc.html', url_root= url_for('home', _external=True, _scheme='http' if is_local_host else 'https'))

if __name__ == '__main__':
    app.run(ssl_context='adhoc')
