from flask import Flask
from flask_sentinel import ResourceOwnerPasswordCredentials, oauth


app = Flask(__name__)
ResourceOwnerPasswordCredentials(app)

# optionally load settings from py module
#app.config.from_object('settings')

@app.route('/endpoint')
@oauth.require_oauth()
def restricted_access():
    return "You made it through and accessed the protected resource!"

@app.route('/')
def home():
    return "hello"

if __name__ == '__main__':
    print "ResourceOwnerPasswordCredentials"
    #ResourceOwnerPasswordCredentials(app)
    #app.run(ssl_context='adhoc')
