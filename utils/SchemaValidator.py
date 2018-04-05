from schema import Schema, Regex, Optional

def validate_userbycredential(data):
    if not data:
        return 400, False, 'post is not in json format or empty'
    try:
        schema = Schema({   'authlogin': basestring,
                            Optional('secret'): basestring,
                            'client_id' : basestring,
                            'provider':  Regex(r'(google|facebook|twitter|woofwoof)')
                        })
        isValid = schema.validate(data)
        return  200 if isValid else 400, isValid, None

    except Exception as e:
        return 400, False, e
