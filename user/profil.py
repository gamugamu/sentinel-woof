# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, request
from flask_sentinel import oauth
from utils import UserHelper as uh
from storage.models import to_json
from utils.UserHelper import petsOwner_from_session
from utils import SchemaValidator as schema
import credential

profil = Blueprint('me_profil', __name__, template_folder='templates')

@profil.route('/me/oauth', methods=['POST'])
def userbycredential():
    # valide que les clès sont bonnes
    code, isValid, errorMessage = schema.validate_userbycredential(request.json)
    token = {}

    if isValid:
        token, errorMessage = credential.conversion(request.json)

    # retourne le compte
    return json.dumps({'token':token, 'error': errorMessage.__str__()}), code

@profil.route('/me/profil')
@oauth.require_oauth()
def me_profil():
    pets_owner, error = petsOwner_from_session()
    # user = TokenBearer.user_from_session()
    # print "info: ", user, str(user._id) #5abcf96104581c4386789968
    if pets_owner is not None:
        return to_json(pets_owner)
    else:
        return error

@profil.route('/me/test')
def me_test():
    #allStation = Station.query.all()
    #station = Station()
    #print "allStation --> ", allStation, len(allStation)
    #db.session.add(station)
    #db.session.commit()
    #return "done-- " + str(len(allStation)) + "---"
    return "test"
