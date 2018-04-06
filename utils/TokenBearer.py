# -*- coding: utf-8 -*-
from flask import request
from flask_sentinel.data import Storage

def user_from_session():
    token = request.headers.get('Authorization')

    if token is not None:
        token_value    = token.replace("Bearer ", "")
        T              = Storage.get_token(token_value)
        return T.user, None
    else:
        return None, "session invalide"
