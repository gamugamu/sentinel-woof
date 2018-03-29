from app import app
from flask_sentinel import ResourceOwnerPasswordCredentials

if __name__ == "__main__":
    print "ResourceOwnerPasswordCredentials"
    ResourceOwnerPasswordCredentials(app)
    app.run()
