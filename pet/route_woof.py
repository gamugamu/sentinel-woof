# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, request
from utils.error import Error, Error_code
import utils.SchemaValidator as schema
import utils.TokenBearer as Token_Bearer
from flask_sentinel import oauth
from werkzeug.routing import BaseConverter
from utils.error import *
from utils.UserHelper import petsOwner_from_session
from images_upload.uploader import bucket_setup

route_woof = Blueprint('route_woof', __name__, template_folder='templates')

class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

@route_woof.route('/<regex("[a-z]{2,10}"):seed>-<_seed>/<regex("[a-z, 0-9]{2,20}"):woof>')
def route_woof_get(seed, _seed, woof):
    from utils.PetsHelper import query_from_woof_name, put_from_sanitized
    from storage.models import Pet

    woof_name   = "%s-%s/%s" % (seed, _seed, woof)
    pet         = query_from_woof_name(woof_name)
    error       = Error()

    if pet is None:
        error.code  = Error_code.PETNOTFD
        pet         = Pet()

    return jsonify({"error" : error.to_dict(), "woof" : sanitizer(pet)})

# Les animaux du petowner. Post pour rajouter.
@route_woof.route('/pets', methods=['POST', 'GET'])
@oauth.require_oauth()
def me_pets():
    from storage.models import PetsOwner, sanitized_collection, commit
    from utils.PetsHelper import new_pet, put_from_sanitized

    error = Error()
    pets  = {}

    try:
        peto = petsOwner_from_session()

        # • Retourne l'utilisateur actuel.
        if request.method == 'GET':
            pets = peto.pets

        # • Modifie l'utilisateur.
        elif request.method == 'POST':
            data        = request.get_json()
            sanitized   = schema.validate_pet(data)
            pet         = new_pet(peto)
            # mutate and save
            put_from_sanitized(sanitized, pet, peto)
            commit()
            pets        = peto.pets

    except ErrorException as e:
        error = e.error

    return jsonify({"error" : error.to_dict(), "pets" : sanitized_collection(pets)})

@route_woof.route('/pet/<pet_name>', methods=['GET', 'PUT'])
@oauth.require_oauth()
def route_woof_put(pet_name):
    from utils.PetsHelper import query_from_pet_name, put_from_sanitized
    from utils.UserHelper import petsOwner_from_session
    from storage.models import Pet, commit, sanitizer

    error = Error()
    pet   = {}
    try:
        peto    = petsOwner_from_session()
        pet     = query_from_pet_name(peto, pet_name)

        if request.method == 'GET':
            pass

        elif request.method == 'PUT':
            data      = request.get_json()
            sanitized = schema.validate_pet(data)
            put_from_sanitized(sanitized, pet, peto)
            commit()

    except ErrorException as e:
        error = e.error
        pet   = {}

    return jsonify({"error" : error.to_dict(), "woof" : sanitizer(pet)})

@route_woof.route('/pet/badge/<pet_name>', methods=['GET', 'PUT'])
@oauth.require_oauth()
def pet_badge(pet_name):
    from images_upload.uploader import upload_file
    from utils.PetsHelper import query_from_pet_name
    from storage.models import commit, sanitizer

    error   = Error()
    pet     = {}

    try:
        peto = petsOwner_from_session()
        pet  = query_from_pet_name(peto, pet_name)
        #TODO validation
        path = upload_file(request.files["file"], bucketName="badges")
        pet.url_badge = path
        commit()

    except ErrorException as e:
        error = e.error

    return jsonify({"error" : error.to_dict(), "woof" : sanitizer(pet)})

route_feed = Blueprint('route_woof', __name__, template_folder='templates')

# FEED
@route_woof.route('/pet/feeds/<pet_name>', methods=['GET', 'POST'])
@oauth.require_oauth()
def feeds(pet_name):
    from images_upload.uploader import upload_file
    from utils.PetsHelper import query_from_pet_name, new_feed

    from storage.models import commit, sanitized_collection

    error   = Error()
    feeds   = {}

    try:
        peto = petsOwner_from_session()
        pet  = query_from_pet_name(peto, pet_name)
        print "pet ", pet, pet.feeds

        if request.method == 'GET':
            feeds   = pet.feeds


        elif request.method == 'POST':
            data    = request.files
            feed    = new_feed(pet)
            feeds   = pet.feeds
            print "new feed? ", feed, pet.to_dict()
            #sanitized = schema.validate_pet(data)
            #put_from_sanitized(sanitized, pet, peto)
            commit()

    except ErrorException as e:
        error = e.error

    return jsonify({"error" : error.to_dict(), "feeds" : sanitized_collection(feeds)})

def route(app):
    app.url_map.converters['regex'] = RegexConverter
    app.register_blueprint(route_woof)
