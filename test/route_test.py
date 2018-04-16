# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, request, url_for
from utils.error import Error, Error_code
import utils.SchemaValidator as schema
import utils.TokenBearer as Token_Bearer
from flask_sentinel import oauth
from werkzeug.routing import BaseConverter
from utils.error import Error, Error_code
import commands
from user.credential import internal_url

route_test = Blueprint('route_test', __name__, template_folder='templates')

# TODO a supprimer en production
@route_test.route('/test/curl_cmd', methods=['GET', 'POST'])
def curl_cmd():
    # Note: Seulement trusted. Sandboxed dans docker
    proxy_url   = url_for('home', _external=True)
    intern_url  = internal_url("/")
    cmd         = request.json['command']

    # curl est appelé en interne dans docker
    print "proxy_url ", proxy_url, "intern_url ", intern_url
    cmd = cmd.replace(proxy_url, intern_url)
    print "*** called command: ", cmd
    cmd += " -s" # silent progress bar
    status, output = commands.getstatusoutput(cmd)
    print "output? ", output
    return output

@route_test.route('/test/a', methods=['GET'])
def testgf():
    err = Error(code=Error_code.NO_OP)
    print "---> ", err
    return "gfd"

def route(app):
    app.register_blueprint(route_test)
