'''
Created on Aug 29, 2011

@author: eric
'''
import logging
import datetime
import transaction

from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_, or_

from motionman.models import DBSession
from motionman.models import User

log = logging.getLogger(__name__)

class DuplicatedName(Exception):
    pass

class DuplicatedEmail(Exception):
    pass

def load_users():
    session = DBSession()
    return session.query(User).filter(User.status==1).all()

def load_user(id):
    session = DBSession()
    return session.query(User).filter(User.id==id).first()

def add_user(name, email, vote_weight):
    session = DBSession()
    
    dup_check = session.query(User).filter(and_(User.status==1,or_(User.name==name, User.email==email))).all()
    if len(dup_check) != 0:
        for i in dup_check:
            if i.name == name:
                raise DuplicatedName()
            if i.email == email:
                raise DuplicatedEmail()

    user = User()
    user.email = email
    user.name = name
    user.vote_weight = vote_weight
    
    try:
        session.add(user)
        session.flush()
        transaction.commit()
    except IntegrityError:
        transaction.abort()

def update_user(id, name, email, vote_weight):
    session = DBSession()
    session.query(User).filter(User.id==id).update({User.name:name,
                                                    User.email:email,
                                                    User.vote_weight:vote_weight})

def delete_user(id):
    session = DBSession()
    session.query(User).filter(User.id==id).update({User.status:0})
