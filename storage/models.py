# -*- coding: utf-8 -*-
from os import environ
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (scoped_session, sessionmaker, relationship,
                            backref)
import datetime

Base        = declarative_base()

def configure(app):
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

class PetsOwner(Base):
    __tablename__   = 'petsowner'
    id              = Column(Integer, primary_key=True)
    sentinel_id     = Column(Integer)
    mail            = Column(String(50))
    seed            = Column(String(20))
    pets            = relationship("Pet", cascade="all, delete-orphan")

class Pet(Base):
    __tablename__   = 'pet'
    id              = Column(Integer, primary_key=True)
    name            = Column(String(20))
    woof_name       = Column(String(41))
    parent_id       = Column(Integer, ForeignKey('petsowner.id'))
