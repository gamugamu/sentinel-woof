# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify
from sqlalchemy.ext.serializer import dumps
from utils.error import Error, Error_code
import json
import utils.SchemaValidator as schema
import utils.TokenBearer as Token_Bearer
from flask_sentinel import oauth
from utils.UserHelper import petsOwner_from_session
from utils.Sanitizer import put_sanitized

route_me = Blueprint('route_me', __name__, template_folder='templates')

# Authentification, récuperation du token session. Création user si null.
@route_me.route('/me/oauth', methods=['POST'])
def me_oauth():
    from utils import SchemaValidator as schema
    import credential

    #detect si un refresh_token
    refresh_token = None
    error         = Error()

    # si c'est un refresh token, on le rafraichit
    if request.json is not None:
        refresh_token = request.json.get("refresh_token")

    if refresh_token is not None:
        sanitized, e = schema.validate_refresh_token(request.json)

        if e is None:
            token   = credential.refresh(sanitized)
            e_str   = token.get("error")

            if e_str is not None:
                # mauvais token
                error.code  = Error_code.INVGRANT
                error.info  = e_str
                token       = {}
        else:
            # mauvais schema
            error.code  = Error_code.MALFSCHE
            error.info  = str(e)

    # c'est une demande de ticket via un provider (google, facebook, twitter)
    else:
        # valide que les clès sont bonnes
        sanitized, e    = schema.validate_userbycredential(request.json)
        token           = {}

        if e is None:
            token, errorMessage = credential.conversion(request.json)
        else:
            error.code  = Error_code.MALFSCHE
            error.info  = str(e)


    # retourne le compte
    return jsonify({"error" : error.to_dict(), "oauth" : token})

# Info utilisateur. Retourne les infos de l'utilisateurs. Mutable sauf le seed.
@route_me.route('/me', methods=['GET', 'PUT', 'DELETE'])
@oauth.require_oauth()
def me_profil():
    from storage.models import PetsOwner, delete_n_commit, commit

    peto, error = petsOwner_from_session()

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
            error.code  = Error_code.MALFSCHE
            error.info  = str(e)

    # • Supprime l'utilisateur.
    elif request.method == 'DELETE':
        delete_n_commit(peto)
        peto = PetsOwner()

    return jsonify({"error" : error.to_dict(), "me" : peto.sanitized()})

# Les animaux du petowner. Post pour rajouter.
@route_me.route('/me/pets', methods=['POST', 'GET'])
def me_pets():
    from storage.models import PetsOwner, sanitized_collection, commit
    from utils.PetsHelper import new_pet, put_from_sanitized

    peto, error = petsOwner_from_session()
    print "peto ", peto
    # • Retourne l'utilisateur actuel.
    if request.method == 'GET':
        pass

    # • Modifie l'utilisateur.
    elif request.method == 'POST':
        data            = request.get_json()
        sanitized, e    = schema.validate_pets(data)
        print "e ", e
        if e is None:
            pet, error = new_pet(peto, error)
            print "e ", error
            if error.code is Error_code.SUCCESS:
                print "sanitized", sanitized, pet
                error = put_from_sanitized(sanitized, pet, peto, error)
                print "name ", pet.name
                print "commited"
                commit()
        else:
            # Blank
            error.code  = Error_code.MALFSCHE
            error.info  = str(e)

    return jsonify({"error" : error.to_dict(), "pets" : sanitized_collection(peto.pets)})
