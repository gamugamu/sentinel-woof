# -*- coding: utf-8 -*-
from flask_sentinel.data import Storage
from flask import url_for
import utils.CredentialValidator as credential
import hashlib
import requests
import json
from utils.UserHelper import user_from_credential, mirrored_petsOwner

def conversion(data):
    # valide que le credential du provider est bon
    provider        = data.get("provider")
    code, user_cloud_info = credential.request_user_info_by_token(
        data.get("authlogin"), data.get("secret"), provider)
    token           = {}
    errorMessage    = ""

    if code == 200:
        #TODO user_info doit être similaire entre woofwoof, google, yahoo, et twitter
        user_id     = user_cloud_info["id"]
        user_pass   = hashlib.sha224(user_id).hexdigest()

        # note: _user est privé. Ne pas exposer aux clients.
        _user   = user_from_credential(user_id, user_pass)
        r       = requests.post(url_for('access_token', _external=True),
                        data = {
                            'client_id' : data["client_id"],
                            'grant_type': 'password',
                            'username'  : user_id,
                            'password'  : user_pass})

        token = json.loads(r.text)
        # le client peut être invalide.
        if "error" in token:
            token = {}
            errorMessage = 'cliend_id is invalid'
        else:
            #Les données sont valides,et on peut en tout sécurité créer
            # ou récupérer le petsowner (petsowner = user loggé)
            T           = Storage.get_token(token["access_token"])
            sent_id     = str(T.user._id)
            # garanti d'être unique. Si le sent_id ne fait pas son taf.
            provider_id = provider + str(user_id)
            # Créer si petowner n'existe pas
            mirrored_petsOwner(sent_id, provider_id)

    # bad credential
    else:
        errorMessage = 'credential is invalid'

    return token, errorMessage

def refresh(data):
    r  = requests.post(url_for('access_token', _external=True),
                data = {
                    'client_id'         : data["client_id"],
                    'grant_type'        : 'refresh_token',
                    'refresh_token'     : data["refresh_token"]})
    token = json.loads(r.text)
    return token
