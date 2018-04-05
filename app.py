# -*- coding: utf-8 -*-
from flask import Flask, request, render_template
from flask_sentinel import ResourceOwnerPasswordCredentials, oauth
import SchemaValidator as schema
import user.credential as credConvertor
import json
from user.profil import profil

app = Flask(__name__)
app.register_blueprint(profil)
ResourceOwnerPasswordCredentials(app)

@app.route('/me/oauth', methods=['POST'])
def userbycredential():
    # valide que les clès sont bonnes
    code, isValid, errorMessage = schema.validate_userbycredential(request.json)
    token = {}

    if isValid:
        token, errorMessage = credConvertor.conversion(request.json)

    # retourne le compte
    return json.dumps({'token':token, 'error': errorMessage.__str__()}), code

@app.route('/')
def home():
    return render_template('doc.html', url_root=request.url_root)

if __name__ == '__main__':
    app.run(ssl_context='adhoc')
