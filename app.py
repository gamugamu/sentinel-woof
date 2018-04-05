# -*- coding: utf-8 -*-
from flask import Flask, request, render_template
from flask_sentinel import ResourceOwnerPasswordCredentials, oauth
import SchemaValidator as schema
import WoofToken_FromCredential as credConvertor
import json
from user.profil import profil

app = Flask(__name__)
app.register_blueprint(profil)
ResourceOwnerPasswordCredentials(app)

# optionally load settings from py module
#app.config.from_object('settings')

@app.route('/endpoint')
@oauth.require_oauth()
def restricted_access():
    return "You made it through and accessed the protected resource!"

@app.route('/me/oauth', methods=['POST'])
def userbycredential():
    # valide que les clès sont bonnes
    code, isValid, errorMessage = schema.validate_userbycredential(request.json)
    token = {}

    if isValid:
        token, errorMessage = credConvertor.credentialConversion(request.json)

    # retourne le compte
    return json.dumps({'token':token, 'error': errorMessage.__str__()}), code

@app.route('/')
def home():
    return render_template('doc.html', url_root=request.url_root)

if __name__ == '__main__':
    app.run(ssl_context='adhoc')
