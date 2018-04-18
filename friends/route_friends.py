# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, request
import utils.SchemaValidator as schema
import utils.TokenBearer as Token_Bearer
from flask_sentinel import oauth
from utils.error import *
from utils.UserHelper import petsOwner_from_session

route_friends = Blueprint('route_friends', __name__, template_folder='templates')

@route_friends.route('/friends', methods=['GET'])
@oauth.require_oauth()
def friends():
    from utils.PetsHelper import query_from_pet_name
    error   = Error()

    return "Hzllo friends"

def route(app):
    app.register_blueprint(route_friends)
