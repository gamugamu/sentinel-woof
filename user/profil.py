# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify
from sqlalchemy.ext.serializer import dumps
from utils.error import Error, Error_code
import json
import utils.SchemaValidator as schema

profil = Blueprint('me_profil', __name__, template_folder='templates')

def json_decorate(func):
   def func_wrapper():
       return jsonify(func())

   return func_wrapper

def put_sanitized(dict, sql):
    for k, v in dict.iteritems():
        setattr(sql, k, v)

# Description des routes /me
# Info utilisateur. POST en privé. GET/PUT/DELETE public.
@profil.route('/me', methods=['GET', 'POST', 'PUT', 'DELETE'])
@json_decorate
#@oauth.require_oauth()
def me_profil():
    from storage.models import PetsOwner, add_n_commit, delete_n_commit, commit
    import petname

    # user = TokenBearer.user_from_session()
    # print "info: ", user, str(user._id) #5abcf96104581c4386789968 #sentinel_id
    peto    = PetsOwner.query.filter_by(mail='-*').first()
    error   = Error()

    # • Retourne l'utilisateur actuel.
    if request.method == 'GET':
        pass

    # • Crée un utilisateur.
    elif request.method == 'POST':
        if peto is None:
            # Devrait n'être appelé qu'en interne. Sinon la session n'existe pas.
            data         = request.get_json()
            sanitized, e = schema.validate_me(data)

            if e is None:
                peto = PetsOwner(seed=petname.Generate(2, "-"))
                put_sanitized(sanitized, peto)
                add_n_commit(peto)
            else:
                # Blank
                error.code  = Error_code.MALFSCHE.value
                error.info  = str(e)
                peto        = PetsOwner()
        else:
            # Exist déjà. (devrait systematiquement arriver).
            error.code = Error_code.NO_OP.value
            error.info = "already exist"

    # • Modifie l'utilisateur.
    elif request.method == 'PUT':
        #TODO a faire
        data = request.get_json()
        peto.mail = data.get("mail")
        commit()

    # • Supprime l'utilisateur.
    elif request.method == 'DELETE':
        delete_n_commit(peto)
        peto = "{}"

    # @json_decorate + oauth
    return {"error" : error.__dict__, "me" : peto.sanitized()}

@profil.route('/me/oauth', methods=['POST'])
def userbycredential():
    from utils import SchemaValidator as schema
    import credential

    # valide que les clès sont bonnes
    code, isValid, errorMessage = schema.validate_userbycredential(request.json)
    token = {}

    if isValid:
        token, errorMessage = credential.conversion(request.json)

    # retourne le compte
    return json.dumps({'token':token, 'error': errorMessage.__str__()}), code
