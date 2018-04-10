# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, request
from utils.error import Error, Error_code
import utils.SchemaValidator as schema
import utils.TokenBearer as Token_Bearer
from flask_sentinel import oauth
from werkzeug.routing import BaseConverter
from utils.error import Error, Error_code

route_woof = Blueprint('route_woof', __name__, template_folder='templates')

class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

#@Route woof-name
@route_woof.route('/<regex("[a-z]{2,10}"):seed>-<_seed>/<regex("[a-z, 0-9]{2,20}"):woof>')
def route_woof_get(seed, _seed, woof):
    from utils.PetsHelper import query_from_woof_name, put_from_sanitized
    from storage.models import Pet
#TODO refactor
    print "%s-%s/%s" % (seed, _seed, woof)
    woof_name   = "%s-%s/%s" % (seed, _seed, woof)
    pet         = query_from_woof_name(woof_name)
    error       = Error()

    if pet is None:
        error.code  = Error_code.PETNOTFD
        error.info  = "Pet not found"
        pet         = Pet()

    print "found? ", pet

    return jsonify({"error" : error.to_dict(), "woof" : pet.sanitized()})

@route_woof.route('/pets/<pet_name>', methods=['PUT'])
@oauth.require_oauth()
def route_woof_put(pet_name):
    from utils.PetsHelper import query_from_woof_name, put_from_sanitized
    from utils.UserHelper import petsOwner_from_session
    from storage.models import Pet, commit

    print "PUT*****"
    #TODO refactor
    peto, error = petsOwner_from_session()
    woof_name   = "%s-%s/%s" % (seed, _seed, woof)
    #TODO refaire recherche

    pet         = query_from_woof_name(woof_name)

    if pet is None:
        error.code  = Error_code.PETNOTFD
        error.info  = "Pet not found"
    else:
        data          = request.get_json()
        sanitized, e  = schema.validate_pet(data)
        put_from_sanitized(sanitized, pet, peto, e)
        print "error ", error, pet
        print "commited"
        commit()

    return jsonify({"error" : error.to_dict(), "woof" : pet.sanitized()})

"""
    sanitized, e    = schema.validate_pets(data)
    print "e ", e
    if e is None:
        pet, error = new_pet(peto, error)
        print "e ", error
        if error.code is Error_code.SUCCESS:
            print "sanitized", sanitized, pet
            error = put_from_sanitized(sanitized, pet, peto, error)
"""
def route(app):
    app.url_map.converters['regex'] = RegexConverter
    app.register_blueprint(route_woof)
