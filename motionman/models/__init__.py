


import datetime
import transaction

from pyramid.security import Allow
from pyramid.security import Everyone

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Unicode
from sqlalchemy import DateTime

from sqlalchemy import ForeignKey
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation, backref
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    email = Column(Unicode(128), nullable=False)
    name = Column(Unicode(16), nullable=False)
    vote_weight = Column(Integer, nullable=True, default=0)
    creator = Column(Integer, nullable=True, default=0)
    create_time = Column(DateTime, nullable=True, default=datetime.datetime.now())
    last_modifier = Column(Integer, nullable=True, default=0)
    last_modify_time = Column(DateTime, nullable=True, default=datetime.datetime.now())
    status = Column(Integer, nullable=True, default=1)    # 0=deleted, 1=active
    
    def __init__(self):
        self.create_time = datetime.datetime.now()
        self.last_modify_time = datetime.datetime.now()


class Setting(Base):
    __tablename__ = 'setting'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(Unicode(64), nullable=False)
    value = Column(Unicode(255), nullable=True, default=u'')
    valuex = Column(Unicode(), nullable=True, default=u'')
    creator = Column(Integer, nullable=True, default=0)
    create_time = Column(DateTime, nullable=True, default=datetime.datetime.now())
    last_modifier = Column(Integer, nullable=True, default=0)
    last_modify_time = Column(DateTime, nullable=True, default=datetime.datetime.now())
    status = Column(Integer, nullable=True, default=1)    # 0=deleted, 1=active

    def __init__(self):
        self.create_time = datetime.datetime.now()
        self.last_modify_time = datetime.datetime.now()


class Motion(Base):
    __tablename__ = 'motion'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    title = Column(Unicode(255), nullable=False)
    desc = Column(Unicode(), nullable=True, default=u'')
    creator = Column(Integer, nullable=True, default=0)
    create_time = Column(DateTime, nullable=True, default=datetime.datetime.now())
    last_modifier = Column(Integer, nullable=True, default=0)
    last_modify_time = Column(DateTime, nullable=True, default=datetime.datetime.now())
    status = Column(Integer, nullable=True, default=1)    # 0=deleted, 1=active
    
    def __init__(self):
        self.create_time = datetime.datetime.now()
        self.last_modify_time = datetime.datetime.now()
        
    def finished(self):
        is_finished = True
        for itm in self.participants:
            if itm.status == 1:
                is_finished = False
        return is_finished

    def weight(self):
        weight = 0
        for itm in self.participants:
            weight += len(itm.chip_list.split('_'))
        return weight
    
    
class MotionOption(Base):
    __tablename__ = 'motion_option'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    motion_id = Column(Integer, ForeignKey('motion.id'), nullable=False)
    value = Column(Unicode(255), nullable=True, default=u'')
    result = Column(Integer, nullable=True, default=0)
    creator = Column(Integer, nullable=True, default=0)
    create_time = Column(DateTime, nullable=True, default=datetime.datetime.now())
    last_modifier = Column(Integer, nullable=True, default=0)
    last_modify_time = Column(DateTime, nullable=True, default=datetime.datetime.now())
    status = Column(Integer, nullable=True, default=1)    # 0=deleted, 1=active
    
    motion = relation(Motion, backref=backref('options', order_by=id))
    
    def __init__(self):
        self.create_time = datetime.datetime.now()
        self.last_modify_time = datetime.datetime.now()
        
    def percent(self):
        opt_percent = 0
        weight = self.motion.weight()
        if weight:
            opt_percent = self.result * 1.0 / weight * 100
        return int(opt_percent)


class MotionParticipant(Base):
    __tablename__ = 'motion_participant'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    motion_id = Column(Integer, ForeignKey('motion.id'), nullable=False)
    user_id = Column(Integer, nullable=False)
    chip_list = Column(Unicode(255), nullable=True, default=u'')
    creator = Column(Integer, nullable=True, default=0)
    create_time = Column(DateTime, nullable=True, default=datetime.datetime.now())
    last_modifier = Column(Integer, nullable=True, default=0)
    last_modify_time = Column(DateTime, nullable=True, default=datetime.datetime.now())
    status = Column(Integer, nullable=True, default=1)    # 0=deleted, 1=active, 2=used

    motion = relation(Motion, backref=backref('participants', order_by=id))
    
    def __init__(self):
        self.create_time = datetime.datetime.now()
        self.last_modify_time = datetime.datetime.now()
    
class MotionMessage(Base):
    __tablename__ = 'motion_message'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    motion_id = Column(Integer, ForeignKey('motion.id'), nullable=False)
    message = Column(Unicode(255), nullable=True, default=u'')
    creator = Column(Integer, nullable=True, default=0)
    create_time = Column(DateTime, nullable=True, default=datetime.datetime.now())
    last_modifier = Column(Integer, nullable=True, default=0)
    last_modify_time = Column(DateTime, nullable=True, default=datetime.datetime.now())
    status = Column(Integer, nullable=True, default=1)

    motion = relation(Motion, backref=backref('messages', order_by=id.desc()))

    def __init__(self):
        self.create_time = datetime.datetime.now()
        self.last_modify_time = datetime.datetime.now()


def initialize_sql(engine):
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)

class RootFactory(object):
    __acl__ = [ (Allow, Everyone, 'view'),
                (Allow, 'group:editors', 'edit'),
                (Allow, 'group:admins', 'manage') ]
    def __init__(self, request):
        pass