# -*- coding: utf-8 -*-
from utils.error import *
from utils.Sanitizer import put_sanitized
from sqlalchemy import and_
from datetime import datetime


def friend_from_request(seed):
    from storage.models import PetsOwner
    return PetsOwner.query.filter(PetsOwner.seed == seed).first()

def pending_friend(peto):
    from storage.models import Friendship

    return Friendship.query.filter(and_(Friendship.user_from == peto.id, Friendship.status == Friendship.Request.PENDING)).all()

def decorate_friends_as_peto(friends):
    from storage.models import Friendship as f_ship
    from storage.models import PetsOwner, sanitizer

    map = []
    for friend in friends:
        map.append(friend.user_from)

    #list_id = {id(x): x for x in friends}
    peto_friends    = PetsOwner.query.filter(PetsOwner.id.in_(map)).all()
    friend_list     = []
    # Note: On part du principe que l'orde la la liste d'id est dans le même
    # ordre que celle de la query. Si la query n'est pas dans l'ordre, on l'a
    # dans le baba.
    for i, peto in enumerate(peto_friends):
        friend = sanitizer(peto)
        friend["status"] = friends[i].status
        friend_list.append(friend)

    return friend_list

def ask_friend(peto, friend):
    from storage.models import Friendship as f_ship

    if friend is None:
        raise ErrorException(Error(code=Error_code.USERNOTFD))
    else:
        rel = f_ship.query.filter(and_(f_ship.user_to == peto.id, f_ship.user_from == friend.id)).first()

        if rel is None:
            # add relation
            rel = f_ship(r_to=peto , r_from=friend, status=f_ship.Request.PENDING)

        # check if both side can be friends
        from_friend = f_ship.query.filter(and_(f_ship.user_to == friend.id, f_ship.user_from == peto.id) ).first()

        if from_friend is not None and from_friend.status == f_ship.Request.PENDING: # PENDING only?
            # friendship is accorded
            from_friend.status  = f_ship.Request.GRANTED
            rel.status          = f_ship.Request.GRANTED

def unfriend(peto, friend):
    if friend in self.friends:
        self.friends.remove(friend)
        friend.friends.remove(self)
