# -*- coding: utf-8 -*-
from flask_sentinel.data import Storage
from flask import url_for
import CredentialValidator as credential
import hashlib
import requests
import UserHelper
import json

def credentialConversion(data):
    # valide que le credential du provider est bon
    code, user_cloud_info = credential.request_user_info_by_token(
        data.get("authlogin"), data.get("secret"), data.get("provider"))
    token           = {}
    errorMessage    = ""

    if code == 200:
        #TODO user_info doit être similaire entre woofwoof, google, yahoo, et twitter
        user_id     = user_cloud_info["id"]
        print "---> id",  user_cloud_info["id"]
        user_pass   = hashlib.sha224(user_id).hexdigest()
        # note: _user est privé. Ne pas exposer aux clients.
        _user = UserHelper.user_from_credential(user_id, user_pass)
        r = requests.post(url_for('access_token', _external=True),
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
            #test
            T = Storage.get_token(token["access_token"])
            print "info: ", T, T.user, str(T.user._id)
    # bad credential
    else:
        errorMessage = 'credential is invalid'

    return token, errorMessage
