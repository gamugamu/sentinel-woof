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
    db.session.commit()

def to_json(obj):
    print "---> ", jsonify(obj)
    return jsonify(obj)

class PetsOwner(db.Model):
    __tablename__   = 'petsowner'
    id              = Column(Integer, primary_key=True)
    sentinel_id     = Column(String(40))
    mail            = Column(String(50))
    seed            = Column(String(20))
    pets            = relationship("Pet", backref='petowner', cascade="all, delete-orphan")

class Pet(db.Model):
    __tablename__   = 'pet'
    id              = Column(Integer, primary_key=True)
    name            = Column(String(20))
    woof_name       = Column(String(41))
    petowner_id     = db.Column(db.Integer, db.ForeignKey('petsowner.id'))
