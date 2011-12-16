'''
Created on 2011-9-19

@author: eryxlee
'''
import logging

from motionman.models import DBSession
from motionman.models import MotionMessage

log = logging.getLogger(__name__)


def add_message(motion_id, message):
    session = DBSession()
    
    mess = MotionMessage()
    mess.motion_id = motion_id
    mess.message = message
        
    session.add(mess)
    session.flush()
