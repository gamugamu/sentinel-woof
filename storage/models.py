# -*- coding: utf-8 -*-
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (scoped_session, sessionmaker, relationship,
                            backref)
import datetime
import json
from app import app
from os import environ

host_name = 'db' if environ.get('NUC') is not None else 'localhost'

#TODO deplacer secret
POSTGRES = {
    'user': 'postgres',
    'pw': 'secretpassword',
    'db': 'woof',
    'host': host_name,
    'port': '5432',
}
postgres_url = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = postgres_url
db = SQLAlchemy(app)

def add_n_commit(object):
    db.session.add(object)
    #TODO refacto si necessaire
    db.session.commit()

def delete_n_commit(object):
    db.session.delete(object)
    #TODO refacto si necessaire
    db.session.commit()

def commit():
    db.session.commit()

def to_json(obj):
    return jsonify(obj)

def merge_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z

def sanitized_collection(list):
    sanitized = []

    for o in list:
        res = o.to_dict()
        del res['id']
        res_c = res.copy()

        for k, v in res.iteritems():
            # clean propriétés privées
            if k.startswith("_"):
                del res_c[k]

        sanitized.append(res_c)

    return sanitized

def put_sanitized(data, obj):
    for k, v in data.iteritems():
        setattr(obj, k, v)
    # test if can mod

    if hasattr(obj, 'mod_date'):
        obj.mod_date = datetime.datetime.now()

def sanitizer(obj):
    if isinstance(obj, dict):
        res = obj
    else:
        #OutputMixin
        res = obj.to_dict()
        # l'id doit être caché
        del res['id']

    res_c = res.copy()
    for k, v in res.iteritems():
        # clean propriétés privées
        if k.startswith("_"):
            del res_c[k]

    return res_c

class OutputMixin(object):
    RELATIONSHIPS_TO_DICT = False

    def __iter__(self):
        return self.to_dict().iteritems()

    def sanitized(self):
        res = self.to_dict()
        # l'id doit être caché
        del res['id']
        res_c = res.copy()
        for k, v in res.iteritems():
            # clean propriétés privées
            if k.startswith("_"):
                del res_c[k]

        return res_c

    def to_dict(self, rel=None, backref=None):
        if rel is None:
            rel = self.RELATIONSHIPS_TO_DICT
        res = {column.key: getattr(self, attr)
               for attr, column in self.__mapper__.c.items()}
        if rel:
            for attr, relation in self.__mapper__.relationships.items():
                # Avoid recursive loop between to tables.
                print "*", attr, relation
                if backref == relation.table:
                    continue
                value = getattr(self, attr)
                if value is None:
                    res[relation.key] = None
                elif relation is "id":
                    print "found ", id
                elif isinstance(value.__class__, DeclarativeMeta):
                    res[relation.key] = value.to_dict(backref=self.__table__)
                else:
                    res[relation.key] = [i.to_dict(backref=self.__table__)
                                         for i in value]
        return res

    def to_json(self, rel=None):
        def extended_encoder(x):
            if isinstance(x, datetime):
                return x.isoformat()
            if isinstance(x, UUID):
                return str(x)
        if rel is None:
            rel = self.RELATIONSHIPS_TO_DICT
        return json.dumps(self.to_dict(rel), default=extended_encoder)

class Friendship(OutputMixin, db.Model):
    class Request(Enum):
        NONE    = 0
        PENDING = 1
        GRANTED = 2
        REFUSED = 3

    __tablename__   = 'friends'
    id              = Column(Integer, primary_key=True, autoincrement=False)
    user_from       = db.Column(db.Integer, db.ForeignKey('petsowner.id'), primary_key=True)
    user_to         = db.Column(db.Integer, db.ForeignKey('petsowner.id'), primary_key=True)
    status          = db.Column(db.Integer, default=Request.NONE)

class PetsOwner(OutputMixin, db.Model):
    __tablename__   = 'petsowner'
    id              = Column(Integer, primary_key=True)
    _sentinel_id    = Column(String(40))
    _provider_id    = Column(String(100)) # peut être nécessaire. Garanti d'être unique et pérènne.
    mail            = Column(String(50), unique=True)
    name            = Column(String(50))
    seed            = Column(String(20))
    cre_date        = Column(DateTime)
    pets            = relationship("Pet", backref='petowner', cascade="all, delete-orphan")
    friends_to      = db.relationship('Friendship', backref='r_to', primaryjoin=id==Friendship.user_to)
    friends_from    = db.relationship('Friendship', backref='r_from', primaryjoin=id==Friendship.user_from )

class Pet(OutputMixin, db.Model):
    __tablename__   = 'pet'
    id              = Column(Integer, primary_key=True)
    name            = Column(String(20))
    url_badge       = Column(String(150))
    woof_name       = Column(String(41))
    _petowner_id    = Column(Integer, ForeignKey('petsowner.id'))
    feeds           = relationship("Feed", backref='pet', cascade="all, delete-orphan")
    cre_date        = Column(DateTime)

class Feed(OutputMixin, db.Model):
    __tablename__   = 'feed'
    id              = Column(Integer, primary_key=True)
    url_feed        = Column(String(150))
    comment         = Column(String(300))
    uuid            = Column(String(124))
    cre_date        = Column(DateTime)
    mod_date        = Column(DateTime)
    _pet_id         = Column(Integer, ForeignKey('pet.id'))
    _petowner_id    = Column(Integer) # low coupled
