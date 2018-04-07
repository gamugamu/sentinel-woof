from schema import Schema, Regex, Optional, Use

def validate_userbycredential(data):
    if not data:
        return 400, False, 'not in json format or empty'
    try:
        schema = Schema({   'authlogin': basestring,
                            Optional('secret'): basestring,
                            'client_id' : basestring,
                            'provider':  Regex(r'(google|facebook|twitter|woofwoof)')
                        })
        return schema.validate(data), None

    except Exception as e:
        return "{}", e

def validate_me(data):
    if not data:
        return "{}", 'not in json format or empty'
    try:
        schema = Schema({   Optional('mail')    : Regex(r'\w+@\w+'),
                            Optional('name')    : basestring
                        }, ignore_extra_keys=True)

        return schema.validate(data), None

    except Exception as e:
        return "{}", e
