# -*- coding: utf-8 -*-
from os import environ
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (scoped_session, sessionmaker, relationship,
                            backref)
import datetime
import json

Base        = declarative_base()
db_session  = None

def configure(app):
    global db_session
    print "will configure"

    host_name = 'db' if environ.get('NUC') is not None else 'localhost'

    POSTGRES = {
        'user': 'postgres',
        'pw': 'secretpassword',
        'db': 'woof',
        'host': host_name,
        'port': '5432',
    }
    postgres_url = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

    engine      = create_engine(postgres_url, convert_unicode = True)
    db_session  = scoped_session(sessionmaker(  autocommit  = False,
                                                autoflush   = False,
                                                bind        = engine))
    Base.query  = db_session.query_property()

    #TODO deplacer pour manage.py
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = postgres_url
    db.init_app(app)
    ######
    print "configured"

db = SQLAlchemy()

def add_n_commit(object):
    db_session.add(object)
    db_session.commit()

# you will need this alchemyencoder where your are calling json.dumps to handle datetime and decimal format
# credit to Joonas @ http://codeandlife.com/2014/12/07/sqlalchemy-results-to-json-the-easy-way/
def alchemyencoder(obj):
    """JSON encoder function for SQLAlchemy special classes."""
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        return float(obj)

def to_json(obj):
    return json.dumps(obj.as_dict(), default=alchemyencoder)

class Model():
    def as_dict(self):
        return { c.name: getattr(self, c.name) for c in self.__table__.columns }

class PetsOwner(Base, Model):
    __tablename__   = 'petsowner'
    id              = Column(Integer, primary_key=True)
    sentinel_id     = Column(String(40))
    mail            = Column(String(50))
    seed            = Column(String(20))
    pets            = relationship("Pet", cascade="all, delete-orphan")

class Pet(Base):
    __tablename__   = 'pet'
    id              = Column(Integer, primary_key=True)
    name            = Column(String(20))
    woof_name       = Column(String(41))
    parent_id       = Column(Integer, ForeignKey('petsowner.id'))
