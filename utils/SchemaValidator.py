# -*- coding: utf-8 -*-
from schema import Schema, Regex, Optional, Use
from utils.error import *

def validate_userbycredential(data):
    try:
        schema = Schema({   'authlogin'         : basestring,
                            Optional('secret')  : basestring,
                            'client_id'         : basestring,
                            'provider'          :  Regex(r'(google|facebook|twitter|woofwoof)')
                        })
        return schema.validate(data)

    except Exception as e:
        error = Error(code=Error_code.MALFSCHE, custom_message=str(e))
        raise ErrorException(error)

def validate_refresh_token(data):
    try:
        schema = Schema({   'client_id'     : basestring,
                            'refresh_token' : basestring
                        })
        return schema.validate(data)

    except Exception as e:
        error = Error(code=Error_code.MALFSCHE, custom_message=str(e))
        raise ErrorException(error)

def validate_me(data):
    if not data:
        return "{}", 'not in json format or empty'
    try:
        schema = Schema({   Optional('mail')    : Regex(r'\w+@\w+'),
                            Optional('name')    : basestring
                        }, ignore_extra_keys=True)

        return schema.validate(data)

    except Exception as e:
        #TODO à faire
        return "{}", e

def validate_pet(data):
    if not data:
        return "{}", 'not in json format or empty'
    try:
        schema = Schema({   'name' : basestring,
                        }, ignore_extra_keys=True)

        return schema.validate(data), None

    except Exception as e:
        #TODO à faire
        return "{}", e
