# -*- coding: utf-8 -*-
from flask_sentinel.data import Storage

# renvoie un compte quoi qu'il arrive. Si le compte n'existe pas en crée un.
# Sauf si c'est un compte woofwoof.
def user_from_credential(name, password):
    user = Storage.get_user(name, password)

    if not user:
        #si pas de user, on le crée
        return Storage.save_user(name, password)
    else:
        return user
