# -*- coding: utf-8 -*-
from utils.error import *
from utils.Sanitizer import put_sanitized
from sqlalchemy import and_
from datetime import datetime

MAX_PET = 20

def new_pet(peto):
    from storage.models import PetsOwner, Pet
    pet = {}

    if peto is not None:
        # limit to a quantity
        if len(peto.pets) <= MAX_PET:
            pet = Pet()
            pet.cre_date = datetime.now()
            peto.pets.append(pet)
        else:
            error = Error(code=Error_code.PETMAXLIM)
            raise ErrorException(error, custom_message="You have too much pets: Limit (%u)" % MAX_PET)

    else:
        error = Error(code=Error_code.USERNOTFD)
        raise ErrorException(error)

    return pet

def is_uuid(uuid_string, version=4):
    try:
        # Si uuid_string est un code hex valide mais pas un uuid valid,
        # UUID() va quand même le convertir en uuid valide. Pour se prémunir
        # de ce problème, on check la version original (sans les tirets) avec
        # le code hex généré qui doivent être les mêmes.
        uid = UUID(uuid_string, version=version)
        return uid.hex == uuid_string.replace('-', '')
    except ValueError:
        return False

def new_feed(pet):
    from storage.models import Pet, Feed
    import uuid

    feed                = Feed()
    feed.pub_date       = datetime.now()
    feed.uuid           = uuid.uuid4()
    feed._petowner_id   = pet._petowner_id
    pet.feeds.append(feed)

    return feed

def query_from_feed_uuid(uuid, peto):
    from storage.models import Feed

    feed = Feed.query.filter(and_(Feed._petowner_id == peto.id, Feed.uuid == uuid)).first()
    if feed is None:
        error = Error(code=Error_code.FEEDNOTFND)
        raise ErrorException(error)
    else:
        return feed


def put_from_sanitized(dict, pet, peto):
    from storage.models import Pet, commit
    import os.path

    if Pet.query.filter(and_(Pet._petowner_id == peto.id, Pet.name == dict["name"])).first():
        error = Error(code=Error_code.PETNAMEEX)
        raise ErrorException(error)
    else:
        put_sanitized(dict, pet)
        pet.woof_name = os.path.join(peto.seed, pet.name)

def query_from_woof_name(woof_name):
    from storage.models import Pet

    return Pet.query.filter_by(woof_name=woof_name).first()

def query_from_pet_name(peto, name):
    from storage.models import Pet

    pet = Pet.query.filter(Pet.name==name, Pet._petowner_id == peto.id).first()

    if pet is None:
        raise ErrorException(Error(code=Error_code.PETNOTFD))
    else:
        return pet
