# -*- coding: utf-8 -*-
from flask import request
from flask_sentinel.data import Storage

from flask import jsonify

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=10, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv          = dict(self.payload or ())
        rv['code']  = self.status_code
        rv['info']  = self.message

        return {"error":rv}

def user_from_session():
    token = request.headers.get('Authorization')
    # Note, ça ne devrait jamais arriver car auth gère la validité du token.
    # Cette clause empêche qu'un client demandeur d'un user-session garanti
    # d'être valide/

    if token is not None:
        token_value    = token.replace("Bearer ", "")
        T              = Storage.get_token(token_value)
        return T.user
    else:
        raise InvalidUsage('Session invalide')
