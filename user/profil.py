# -*- coding: utf-8 -*-
from flask import Blueprint
from flask_sentinel import oauth
from utils import TokenBearer

profil = Blueprint('me_profil', __name__, template_folder='templates')

@profil.route('/me/profil')
@oauth.require_oauth()
def me_profil():
    user = TokenBearer.user_from_session()
    print "info: ", user, str(user._id) #5abcf96104581c4386789968

    return "You made it through and accessed the protected resource!"
