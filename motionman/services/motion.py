'''
Created on 2011-9-19

@author: eryxlee
'''
import logging

import random
import transaction

from sqlalchemy.exc import DataError
from sqlalchemy import and_, or_, desc

from motionman.models import DBSession
from motionman.models import User, Motion, MotionOption, MotionParticipant

log = logging.getLogger(__name__)

CHIP_PATTERN = 'abcdefghijklmnopqrstuvwxyz1234567890'

def load_motions(offset, limit):
    session = DBSession()
    
    motion_list = session.query(Motion).filter(Motion.status<>0).order_by(desc(Motion.create_time))

    if offset:
        motion_list = motion_list.offset(offset)
    if limit:
        motion_list = motion_list.limit(limit)
    
    return motion_list.all()

def get_motions_count():
    session = DBSession()
    
    return session.query(Motion).filter(Motion.status<>0).count()    

def load_motion(motion_id):
    session = DBSession()
    return session.query(Motion).filter(Motion.id==motion_id).first()

def add_motion(title, desc, options, users):
    session = DBSession()
    all_users = session.query(User).filter(User.status==1).all()
    
    transaction.begin()
    try:
        motion = Motion()
        motion.title = title
        motion.desc = desc
        
        session.add(motion)
        session.flush()
        
        for opt in options:
            option = MotionOption()
            option.motion_id = motion.id
            option.value = opt
            option.result = 0
            session.add(option)
            
        for user in all_users:
            if user.id in users:
                participant = MotionParticipant()
                participant.motion_id = motion.id
                participant.user_id = user.id
                chips = '_'.join([''.join(random.sample(CHIP_PATTERN, 5)) 
                                  for _ in range(user.vote_weight)])
                participant.chip_list = chips
                session.add(participant)

        session.flush()
        transaction.commit()
    except Exception:
        transaction.abort()


def get_motion_participant_by_chips(motion_id, chips):
    session = DBSession()
    return session.query(MotionParticipant).filter(and_(MotionParticipant.motion_id==motion_id,
                                                        MotionParticipant.chip_list==chips)).first()

def save_vote_result(motion_id, option_id, chips):
    session = DBSession()
    vote_weight = len(chips.split('_'))
    
    transaction.begin()
    try:
        session.query(MotionParticipant).filter(and_(MotionParticipant.motion_id==motion_id,
                                                     MotionParticipant.chip_list==chips)) \
                                        .update({MotionParticipant.status:2})
                                        
        session.query(MotionOption).filter(and_(MotionOption.motion_id==motion_id,
                                                MotionOption.id==option_id)) \
                                   .update({MotionOption.result:MotionOption.result+vote_weight})

        session.flush()
        transaction.commit()
    except Exception:
        transaction.abort()                                                     


