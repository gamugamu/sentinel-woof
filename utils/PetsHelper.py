# -*- coding: utf-8 -*-
from utils.error import Error, Error_code
MAX_PET = 20

def new_pet(peto, error):
    from storage.models import PetsOwner, Pet, add_n_commit
    pet     = {}
    print "T ", error.code, Error_code.SUCCESS
    if peto is not None and error.code is Error_code.SUCCESS:
        # limit to a quantity
        if len(peto.pets) <= MAX_PET:
            pet = Pet()
            peto.pets.append(pet)
        else:
            print "too much pets!"
            error.code  = Error_code.PETMAXLIM
            error.info  = "You have too much pets: Limit (%u)" % MAX_PET

    else:
        error.code  = Error_code.USERNOTFD
        error.info  = "User not found. Did you delete it? (-X DELETE /me). You need to relogin again with a provider token (/me/oauth) and a new user will be recreated"

    return pet, error

def put_from_sanitized(dict, pet, peto, error):
    from storage.models import Pet, commit
    from utils.Sanitizer import put_sanitized
    from sqlalchemy import and_
    import os.path

    print "exist? ", Pet.query.filter(and_(Pet._petowner_id == peto.id, Pet.name == dict["name"])).first()
    if Pet.query.filter(and_(Pet._petowner_id == peto.id, Pet.name == dict["name"])).first():
        error.code  = Error_code.PETNAMEEX
        error.info  = "pet name already exist"
    else:
        put_sanitized(dict, pet)
        pet.woof_name = os.path.join(peto.seed, pet.name)

    return error
