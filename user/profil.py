# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify
from sqlalchemy.ext.serializer import dumps
import json

profil = Blueprint('me_profil', __name__, template_folder='templates')

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

@profil.route('/me/profil', methods=['GET', 'PUT', 'DELETE'])
#@oauth.require_oauth()
def me_profil():
    from storage.models import PetsOwner, add_n_commit, delete_n_commit, commit
    import petname
    peto = PetsOwner.query.filter_by(mail='jiljl').first()
    # TODO, à retirer, Devrait toujours etre evalué a true puisqu' oauth
    if peto is None:
        peto = PetsOwner(mail='kook', seed=petname.Generate(2, "-"))
        add_n_commit(peto)

    # retourne l'utilisateur actuel.
    if request.method == 'GET':
        # devrait toujours retourner un user grace à oauth
        print "total: ",  PetsOwner.query.all()
        return peto.to_json()

    # modifie l'utilisateur
    elif request.method == 'PUT':
        data = request.get_json()
        print "modify", data.get("mail")
        peto.mail = data.get("mail")
        commit()
        # devrait toujours retourner un user grace à oauth
        return peto.to_json()

    elif request.method == 'DELETE':
        # devrait toujours retourner un user grace à oauth
        delete_n_commit(peto)
        print "will delete"
        return "{}"
    """
    # user = TokenBearer.user_from_session()
    # print "info: ", user, str(user._id) #5abcf96104581c4386789968
    if pets_owner is not None:
        return to_json(pets_owner)
    else:
        return error
"""
@profil.route('/me/test')
def me_test():
    #allStation = Station.query.all()
    #station = Station()
    #print "allStation --> ", allStation, len(allStation)
    #db.session.add(station)
    #db.session.commit()
    #return "done-- " + str(len(allStation)) + "---"
    return "test"
