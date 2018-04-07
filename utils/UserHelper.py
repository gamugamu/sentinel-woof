# -*- coding: utf-8 -*-
from flask_sentinel.data import Storage
#from utils import TokenBearer

# renvoie un compte quoi qu'il arrive. Si le compte n'existe pas en crée un.
# Sauf si c'est un compte woofwoof.
def user_from_credential(name, password):
    user = Storage.get_user(name, password)

    if not user:
        #si pas de user, on le crée
        return Storage.save_user(name, password)
    else:
        return user

# copy l'utilisateur
def mirrored_petsOwner(sentinel_id):
    from storage.models import PetsOwner, add_n_commit, commit
    string_id   = str(sentinel_id)
    pets_owner  = PetsOwner.query.filter_by(_sentinel_id=string_id).first()

    if not pets_owner:
        #si pas de user, on le crée
        print "*****CREATE USER"
        pets_owner = PetsOwner(_sentinel_id=string_id)
        add_n_commit(pets_owner)

        return pets_owner
    else:
        return pets_owner

# copy l'utilisateur
def petsOwner_from_session():
    from storage.models import PetsOwner, add_n_commit, commit
    import utils.TokenBearer as Token_Bearer

    user    = Token_Bearer.user_from_session() #@raise
    sent_id = str(user._id)
    peto    = PetsOwner.query.filter_by(_sentinel_id=sent_id).first()

    return peto
