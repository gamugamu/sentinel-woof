# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, request
from utils.error import Error, Error_code
import utils.SchemaValidator as schema
import utils.TokenBearer as Token_Bearer
from flask_sentinel import oauth
from werkzeug.routing import BaseConverter
from utils.error import Error, Error_code
import commands

route_test = Blueprint('route_test', __name__, template_folder='templates')

# TODO a supprimer en production
@route_test.route('/test/curl_cmd', methods=['GET', 'POST'])
def curl_cmd():
    # Note: Seulement trusted. Sandboxed dans docker
    cmd = request.json['command']
    cmd += " -s" # silent progress bar
    status, output = commands.getstatusoutput(cmd)

    return output

@route_test.route('/test/a', methods=['GET'])
def testgf():
    err = Error(code=Error_code.NO_OP)
    print "---> ", err
    return "gfd"

def route(app):
    app.register_blueprint(route_test)
