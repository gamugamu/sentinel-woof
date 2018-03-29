# -*- coding: utf-8 -*-
from flask import Flask, request
from flask_sentinel import ResourceOwnerPasswordCredentials, oauth
from flask_sentinel.data import Storage
import SchemaValidator as schema
#TODO clean
import CredentialValidator as credential
import UserHelper
import json
import hashlib
import requests

from flask_sentinel.data import Storage

app = Flask(__name__)
ResourceOwnerPasswordCredentials(app)

# optionally load settings from py module
#app.config.from_object('settings')

@app.route('/endpoint')
@oauth.require_oauth()
def restricted_access():
    return "You made it through and accessed the protected resource!"

@app.route('/userbycredential', methods=['POST'])
def userbycredential():
    # valide que les clès sont bonnes
    code, isValid, errorMessage = schema.validate_userbycredential(request.json)
    token = {}

    if isValid:
        data = request.json
        # valide que le credential du provider est bon
        code, user_cloud_info = credential.request_user_info_by_token(data["token"], data["provider"])

        if code == 200:
            #TODO user_info doit être similaire entre woofwoof, google, yahoo, et twitter
            user_id     = user_cloud_info["id"]
            user_pass   = hashlib.sha224(user_id).hexdigest()
            # note: _user est privé. Ne pas exposer aux clients.
            _user       = UserHelper.user_from_credential(user_id, user_pass)
            r           = requests.post("http://localhost:5000/oauth/token",
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

    # retourne le compte
    return json.dumps({'token':token, 'error': errorMessage.__str__()}), code

@app.route('/')
def home():
    return "hello"

if __name__ == '__main__':
    app.run(ssl_context='adhoc')
