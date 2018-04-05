# -*- coding: utf-8 -*-
from flask import Flask, request, render_template
from flask_sentinel import ResourceOwnerPasswordCredentials, oauth
import utils.SchemaValidator as schema
import user.credential as credConvertor
import json
from user.profil import profil
from storage.models import storage_configure

app = Flask(__name__)
app.register_blueprint(profil)
ResourceOwnerPasswordCredentials(app)
app.config['DEBUG'] = True
storage_configure(app)

@app.route('/')
def home():
    return render_template('doc.html', url_root=request.url_root)

if __name__ == '__main__':
    app.run(ssl_context='adhoc')
