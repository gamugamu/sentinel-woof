# -*- coding: utf-8 -*-
from flask import Flask, request
from flask_sentinel import ResourceOwnerPasswordCredentials, oauth
from flask_sentinel.data import Storage
import SchemaValidator as schema
import CredentialValidator as credential
import UserHelper
import json
import hashlib

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
    user = {}

    if isValid:
        data = request.json
        # valide que le credential du provider est bon
        code, user_cloud_info = credential.request_user_info_by_token(data["token"], data["provider"])

        if code == 200:
            #TODO user_info doit être similaire entre woofwoof, google, yahoo, et twitter
            user_id = user_cloud_info["id"]
            _user   = UserHelper.user_from_credential(user_id, hashlib.sha224(user_id).hexdigest())
            # note: _user est privé! A ne pas exposer
            user['username'] = _user._username
        # bad credential
        else:
            print "something went bad. Abort"
            errorMessage = 'credential is invalid'

    # retourne le compte
    return json.dumps({'user':user, 'error': errorMessage.__str__()}), code

@app.route('/')
def home():
    return "hello"

if __name__ == '__main__':
    app.run(ssl_context='adhoc')
