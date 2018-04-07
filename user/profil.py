# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify
from sqlalchemy.ext.serializer import dumps
from utils.error import Error, Error_code
import json
import utils.SchemaValidator as schema
import utils.TokenBearer as Token_Bearer
from flask_sentinel import oauth
from utils.UserHelper import petsOwner_from_session

profil = Blueprint('me_profil', __name__, template_folder='templates')

def put_sanitized(dict, sql):
    for k, v in dict.iteritems():
        setattr(sql, k, v)

# Description des routes /me
# Info utilisateur. POST en privé. GET/PUT/DELETE public.
@profil.route('/me', methods=['GET', 'PUT', 'DELETE'])
@oauth.require_oauth()
def me_profil():
    from storage.models import PetsOwner, add_n_commit, delete_n_commit, commit
    peto    = petsOwner_from_session()
    error   = Error()

    # • Retourne l'utilisateur actuel.
    if request.method == 'GET':
        pass

    # • Modifie l'utilisateur.
    elif request.method == 'PUT':
        data            = request.get_json()
        sanitized, e    = schema.validate_me(data)

        if e is None:
            put_sanitized(sanitized, peto)
            commit()
        else:
            # Blank
            error.code  = Error_code.MALFSCHE.value
            error.info  = str(e)
            peto        = PetsOwner()

    # • Supprime l'utilisateur.
    elif request.method == 'DELETE':
        delete_n_commit(peto)
        peto = PetsOwner()

    # @json_decorate + oauth
    return jsonify({"error" : error.__dict__, "me" : peto.sanitized()})

@profil.route('/me/oauth', methods=['POST'])
def userbycredential():
    from utils import SchemaValidator as schema
    import credential
    # valide que les clès sont bonnes
    sanitized, e    = schema.validate_userbycredential(request.json)
    token           = {}
    error           = Error()

    if e is None:
        token, errorMessage = credential.conversion(request.json)
    else:
        error.code  = Error_code.MALFSCHE.value
        error.info  = str(e)


    # retourne le compte
    return jsonify({"error" : error.__dict__, "oauth" : token})
