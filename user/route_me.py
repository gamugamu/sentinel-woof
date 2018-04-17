# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify
from sqlalchemy.ext.serializer import dumps
from utils.error import *
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

    error = Error()
    token = {}
    try:
        refresh_token = request.json.get("refresh_token")
        print "refresh_token ", refresh_token
        # Si c'est un refresh token, on le rafraichit
        if refresh_token is not None:
            sanitized   = schema.validate_refresh_token(request.json)
            token       = credential.refresh(sanitized)
        # Sinon c'est une demande de ticket via un provider (google, facebook, twitter)
        else:
            # valide que les clès sont bonnes
            sanitized   = schema.validate_userbycredential(request.json)
            token       = credential.conversion(sanitized)

    except ErrorException as e:
        error = e.error
    # retourne le compte
    return jsonify({"error" : error.to_dict(), "oauth" : token})

# Info utilisateur. Retourne les infos de l'utilisateurs. Mutable sauf le seed.
@route_me.route('/me', methods=['GET', 'PUT', 'DELETE'])
@oauth.require_oauth()
def me_profil():
    from storage.models import PetsOwner, delete_n_commit, sanitizer, commit

    error = Error()
    peto  = {}
    try:
        peto = petsOwner_from_session()
        # • Retourne l'utilisateur actuel.
        if request.method == 'GET':
            pass

        # • Modifie l'utilisateur.
        elif request.method == 'PUT':
                data       = request.get_json()
                sanitized  = schema.validate_me(data)
                put_sanitized(sanitized, peto)
                commit()

        # • Supprime l'utilisateur.
        elif request.method == 'DELETE':
            delete_n_commit(peto)
            peto = PetsOwner()

    except ErrorException as e:
        error = e.error

    return jsonify({"error" : error.to_dict(), "me" : sanitizer(peto)})
