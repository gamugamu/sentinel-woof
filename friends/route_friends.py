# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, request
import utils.SchemaValidator as schema
import utils.TokenBearer as Token_Bearer
from flask_sentinel import oauth
from utils.error import *
from utils.UserHelper import petsOwner_from_session

route_friends = Blueprint('route_friends', __name__, template_folder='templates')

@route_friends.route('/friends/<friend>', methods=['POST']) # friend = woof_name
@route_friends.route('/friends', defaults={'friend': None}, methods=['GET'])
@oauth.require_oauth()
def friends(friend):
    from utils.PetsHelper import query_from_pet_name
    from utils.FriendsHelper import pending_friend, friend_from_request, ask_friend, decorate_friends_as_peto
    from storage.models import sanitized_collection, commit

    error   = Error()
    friends = {}

    try:
        peto = petsOwner_from_session()
        # friends list
        if request.method == 'GET':
            pass

        # add friend
        if request.method == 'POST':
            # check first that he won't add himself
            seed = friend # label
            if seed == peto.seed:
                # can't add himself
                raise ErrorException(Error(code=Error_code.FRNDALONE))
            else:
                # add friend
                friend = friend_from_request(seed)
                ask_friend(peto=peto, friend=friend)
                commit()

    except ErrorException as e:
        error = e.error
        pet   = {}

    # decorate friends as petowner. Sinon le client devra récupérer chaque id
    # de la liste des friends.
    friends = decorate_friends_as_peto(peto.friends_to)
    return jsonify({"error" : error.to_dict(), "friends" : friends})

def route(app):
    app.register_blueprint(route_friends)
