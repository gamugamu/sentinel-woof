# -*- coding: utf-8 -*-
from utils.error import *
from utils.Sanitizer import put_sanitized

MAX_PET = 20

def new_pet(peto):
    from storage.models import PetsOwner, Pet
    pet = {}

    if peto is not None:
        # limit to a quantity
        if len(peto.pets) <= MAX_PET:
            pet = Pet()
            peto.pets.append(pet)
        else:
            error = Error(code=Error_code.PETMAXLIM)
            raise ErrorException(error, custom_message="You have too much pets: Limit (%u)" % MAX_PET)

    else:
        error = Error(code=Error_code.USERNOTFD)
        raise ErrorException(error)

    return pet

def new_feed(pet):
    from storage.models import Pet, Feed

    feed = Feed()
    feed.comment = "un comment***"
    pet.feeds.append(feed)

    return feed

def put_from_sanitized(dict, pet, peto):
    from storage.models import Pet, commit
    from sqlalchemy import and_
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
