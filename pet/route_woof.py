# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, request
import utils.SchemaValidator as schema
import utils.TokenBearer as Token_Bearer
from flask_sentinel import oauth
from werkzeug.routing import BaseConverter
from utils.error import *
from utils.UserHelper import petsOwner_from_session
from images_upload.uploader import bucket_setup, Bucket

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
def pets():
    from storage.models import PetsOwner, sanitized_collection, commit, put_sanitized
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


@route_woof.route('/pets/badge/<pet_name>', methods=['GET', 'PUT', 'DELETE'])
@oauth.require_oauth()
def pets_badge(pet_name):
    from images_upload.uploader import upload_file
    from utils.PetsHelper import query_from_pet_name
    from storage.models import commit, sanitizer
    error   = Error()
    pet     = {}

    try:
        peto = petsOwner_from_session()
        pet  = query_from_pet_name(peto, pet_name)

        if request.method == 'GET':
            pass

        elif request.method == 'PUT':
            #TODO validation
            path = upload_file(request.files["image"], bucketName=Bucket.BADGE.value)
            pet.url_badge = path
            commit()

        elif request.method == 'DELETE':
            #TODO validation
            path = upload_file(request.files["image"], bucketName=Bucket.BADGE.value)
            pet.url_badge = path
            commit()

    except ErrorException as e:
        error = e.error

    return jsonify({"error" : error.to_dict(), "woof" : sanitizer(pet)})

@route_woof.route('/pets/<pet_name>', methods=['GET', 'PUT', 'DELETE'])
@oauth.require_oauth()
def pets_pet(pet_name):
    from utils.PetsHelper import query_from_pet_name, put_from_sanitized
    from utils.UserHelper import petsOwner_from_session
    from storage.models import Pet, commit, delete_n_commit, sanitizer

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

        elif request.method == 'DELETE':
            delete_n_commit(pet)
            pet = {}

    except ErrorException as e:
        error = e.error
        pet   = {}

    return jsonify({"error" : error.to_dict(), "woof" : sanitizer(pet)})

route_feed = Blueprint('route_feed', __name__, template_folder='templates')

# FEED

@route_feed.route('/feeds/<pet_name>/<current_page>')
@route_feed.route('/feeds/<pet_name>', defaults={'current_page': 1},  methods=['GET', 'POST', 'PUT', 'DELETE'])
@route_feed.route('/feeds', defaults={'pet_name': 1, 'current_page': 1}, methods=['GET'])
@oauth.require_oauth()
def pets_feeds(pet_name, current_page):
    from images_upload.uploader import upload_file
    from utils.PetsHelper import query_from_pet_name, new_feed, query_from_feed_uuid
    from storage.models import commit, sanitized_collection, merge_dicts, put_sanitized
    from storage.models import Feed, delete_n_commit
    from sqlalchemy import and_, desc


    error = Error()
    feeds = {}
    pages = {}

    try:
        def represents_int(s):
            try:
                int(s)
                return True
            except ValueError:
                return False

        if represents_int(pet_name):
            raise ErrorException(Error(code=Error_code.NOTIMPL))

        if isinstance(pet_name, int):
            raise ErrorException(Error(code=Error_code.NOTIMPL))

        peto = petsOwner_from_session()

        if request.method == 'GET':
            pet = query_from_pet_name(peto, pet_name)

            try:
                print "current page", current_page
                _pages  = Feed.query.filter(and_(Feed._pet_id == pet.id)).order_by(desc(Feed.cre_date)).paginate(page=int(current_page), per_page=10)
                feeds   = _pages.items
                #TODO refactor!
                pages = {"total": _pages.total, "page": _pages.page, "per_page": _pages.per_page}
            except: # No op.
                raise ErrorException(Error(code=Error_code.OUTOFSCOPE))

        elif request.method == 'POST':
            pet         = query_from_pet_name(peto, pet_name)
            data        = merge_dicts(request.files, request.form)
            sanitized   = schema.validate_feed(data)
            feed        = new_feed(pet)

            try:
                path = upload_file(sanitized["image"], bucketName=Bucket.FEEDS.value)
            except: # No op.
                raise ErrorException(Error(code=Error_code.WRGDCTYPE))

            # sanitize
            sanitized["url_feed"] = path
            del sanitized["image"]

            put_sanitized(sanitized, feed)
            commit()
            feeds = [feed] # on ne retourne que le post updaté

        elif request.method == 'PUT':
            uuid        = pet_name # label change
            data        = merge_dicts(request.files, request.form)
            sanitized   = schema.validate_feed(data, image_optional=True)
            feed        = query_from_feed_uuid(uuid, peto)
            # note: Les orphan link sont enlevé par un deamon par cycles
            try:
                put_sanitized(sanitized, feed)
            except: # No op.
                raise ErrorException(Error(code=Error_code.WRGDCTYPE))
            commit()
            feeds = [feed]

        elif request.method == 'DELETE':
            uuid        = pet_name # change label
            feed        = query_from_feed_uuid(uuid, peto)
            delete_n_commit(feed)

    except ErrorException as e:
        error = e.error

    result_list = { "error" : error.to_dict(),
                    "feeds" : sanitized_collection(feeds),
                    "pages" : pages}

    return jsonify(result_list)

def route(app):
    app.url_map.converters['regex'] = RegexConverter
    app.register_blueprint(route_woof)
    app.register_blueprint(route_feed)
