# -*- coding: utf-8 -*-
from schema import Schema, Regex, Optional, Use, And
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
    try:
        schema = Schema({   Optional('mail')    : Regex(r'\w+@\w+'),
                            Optional('name')    : basestring
                        }, ignore_extra_keys=True)

        return schema.validate(data)

    except Exception as e:
        error = Error(code=Error_code.MALFSCHE, custom_message=str(e))
        raise ErrorException(error)

def validate_pet(data):
    try:
        schema = Schema({   'name' : basestring,
                        }, ignore_extra_keys=True)

        return schema.validate(data)

    except Exception as e:
        error = Error(code=Error_code.MALFSCHE, custom_message=str(e))
        raise ErrorException(error)

def validate_signin(data, image_optional=False):
    from werkzeug.datastructures import FileStorage

    try:
        schema = Schema({
                            'mail'      : Regex(r'\w+@\w+'),
                            'password'  : Regex(r'^(?=^.{10,}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?)'),
                            'client_id' : basestring,
                            'uuid'      : basestring,
                            'value'     : basestring
                        })


        return schema.validate(data)

    except Exception as e:
        print "error ", e
        error = Error(code=Error_code.MALFSCHE, custom_message=str(e))
        raise ErrorException(error)
