from flask import Flask, request
from flask_sentinel import ResourceOwnerPasswordCredentials, oauth
from flask_sentinel.data import Storage
import json

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
    if not request.json:
        abort(400)

    return json.dumps(request.json)
    #Storage.save_user("***test", "password")

@app.route('/')
def home():
    return "hello"

if __name__ == '__main__':
    app.run(ssl_context='adhoc')
