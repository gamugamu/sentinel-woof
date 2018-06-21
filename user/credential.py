# -*- coding: utf-8 -*-
from flask_sentinel.data import Storage
from flask import url_for
import utils.CredentialValidator as credential
from utils.error import *
import hashlib
import requests
import json
from utils.UserHelper import user_from_credential, mirrored_petsOwner
from os import environ

def internal_url(uri):
    #TODO, be static
    if uri.startswith('/'):
        uri = uri[1:]

    external_url  = environ.get('INTERNAL_URL')
    url           = (external_url if external_url is not None else url_for('home', _external=True)) + uri
    return url

def conversion(data):
    # valide que le credential du provider est bon
    try:
        print "COnversion*** ", data
        provider        = data.get("provider")
        user_cloud_info = credential.request_user_info_by_token(data.get("authlogin"), data.get("secret"), provider)
        token           = {}
        print "++++ convert ?", user_cloud_info

        #TODO user_info doit être similaire entre woofwoof, google, yahoo, et twitter
        user_id         = user_cloud_info["id"]
        has_password    = hasattr(user_cloud_info, "password")
        user_pass       = hashlib.sha224( user_cloud_info["password"] if has_password else user_id ).hexdigest()
        # note: _user est privé. Ne pas exposer aux clients.
        # *** Fait l'authentification côté serveur ***
        _user   = user_from_credential(user_id, user_pass)
        r       = requests.post(internal_url(url_for('access_token')),
                        data = {
                            'client_id' : data["client_id"],
                            'grant_type': 'password',
                            'username'  : user_id,
                            'password'  : user_pass})

        token = json.loads(r.text)
        # le client peut être invalide.
        if "error" in token:
            print "∆ error"
            raise ErrorException(Error(code=Error_code.MALFSCHE, custom_message=token["error"]))
        else:
            print "found token ?", token
            #Les données sont valides,et on peut en tout sécurité créer
            # ou récupérer le petsowner (petsowner = user loggé)
            T           = Storage.get_token(token["access_token"])
            sent_id     = str(T.user._id)
            # garanti d'être unique. Si le sent_id ne fait pas son taf.
            provider_id = provider + str(user_id)
            # Créer si petowner n'existe pas
            mirrored_petsOwner(sent_id, provider_id)
            #TODO: gestion du scope
            token["scope"] = "user:mutable"

    #pass. Rethrow
    except ErrorException as e:
        raise e

    return token


def refresh(data):
    """ rafraichit le token """
    r  = requests.post(internal_url(url_for('access_token')),
                data = {
                    'client_id'         : data["client_id"],
                    'grant_type'        : 'refresh_token',

                    'refresh_token'     : data["refresh_token"]})
    token = json.loads(r.text)

    if token.get("error") is not None:
        # mauvais token
        raise ErrorException(Error(code=Error_code.INVGRANT))

def create_account_session(client_id, user_id, user_pass):
    try:
        _user   = user_from_credential(user_id, user_pass)
        r       = requests.post(internal_url(url_for('access_token')),
                        data = {
                            'client_id' : client_id,
                            'grant_type': 'password',
                            'username'  : user_id,
                            'password'  : user_pass})

        token = json.loads(r.text)
        # le client peut être invalide.
        if "error" in token:
            print "∆ error"
            raise ErrorException(Error(code=Error_code.MALFSCHE, custom_message=token["error"]))
        else:
            print "found token ?", token
            #Les données sont valides,et on peut en tout sécurité créer
            # ou récupérer le petsowner (petsowner = user loggé)
            T           = Storage.get_token(token["access_token"])
            sent_id     = str(T.user._id)
            # garanti d'être unique. Si le sent_id ne fait pas son taf.
            # Créer si petowner n'existe pas
            mirrored_petsOwner(T.user._id, user_pass)
            #TODO: gestion du scope
            token["scope"] = "user:mutable"
    #pass. Rethrow
    except ErrorException as e:
        raise e

    return token
