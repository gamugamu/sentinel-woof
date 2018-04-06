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
    string_id   = str(sentinel_id)
    pets_owner  = PetsOwner.query.filter_by(sentinel_id=string_id).first()

    if not pets_owner:
        #si pas de user, on le crée
        pets_owner = PetsOwner(sentinel_id=string_id)
        add_n_commit(pets_owner)

        return pets_owner
    else:
        return pets_owner

# copy l'utilisateur
def petsOwner_from_session():
    from storage.models import PetsOwner, add_n_commit
    #peto = PetsOwner(mail='kook')
    peto = PetsOwner.query.filter_by(mail='kook').first()
    if peto is None:
        peto = PetsOwner(mail='kook')
        add_n_commit(peto)

    print "peto ", peto.mail, peto.id
    return peto, peto
    """
    user, error = TokenBearer.user_from_session()
    pets_owner  = None

    if error is None:
        pets_owner  = PetsOwner.query.filter_by(sentinel_id=str(user._id)).first()

    return pets_owner, error
    """
