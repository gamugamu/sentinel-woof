# -*- coding: utf-8 -*-
import httplib2
import json
from oauth2client.client import AccessTokenCredentials

def request_user_info_by_token(token, validator):
    credentials = AccessTokenCredentials(token, 'user-agent-value')
    # Si c'est un compte local (woofwoof) alors il faut vérifier que la clès du compte existe
    # Si la clès n'existe pas, le compte n'existe pas

    return request_user_info_google(credentials)

def request_user_info_google(credentials):
    """
    Makes an HTTP request to the Google+ API to retrieve the user's basic
    profile information, including full name and photo, and stores it in the
    Flask session.
    """
    http            = httplib2.Http()
    credentials.authorize(http)

    try:
        resp, content   = http.request('https://www.googleapis.com/plus/v1/people/me')

        if resp.status != 200:
            return resp.status, "Error while obtaining user profile: \n%s: %s" % resp, content

        profil = json.loads(content.decode('utf-8'))
        return resp.status, profil
    # mauvais token
    except Exception as e:
        return 400, e
