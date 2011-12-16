'''
Created on Aug 28, 2011

@author: eric
'''
import copy
import datetime
import transaction

from sqlalchemy.exc import IntegrityError

from motionman.models import DBSession

def init_data():
    from motionman.models import Setting

    session = DBSession()

    setting_orig = Setting()
    setting_orig.id = 1
    setting_orig.name = u"motion_id_prefix"
    setting_orig.value = u"mm"
    setting_orig.valuex = u""
    setting_orig.creator = 0
    setting_orig.create_time = datetime.datetime.now()
    setting_orig.last_modifier = 0
    setting_orig.last_modify_time = datetime.datetime.now()
    setting_orig.status = 1
        
    setting_1 = copy.deepcopy(setting_orig)

    try:
        session.add(setting_1)
        session.flush()
        transaction.commit()
    except IntegrityError:
        transaction.abort()
        
    
    setting_2 = copy.deepcopy(setting_orig)

    setting_2.id = 2
    setting_2.name = u"admin_password"
    setting_2.value = u"123456"
    
    try:
        session.add(setting_2)
        session.flush()
        transaction.commit()
    except IntegrityError:
        transaction.abort()

    setting_3 = copy.deepcopy(setting_orig)

    setting_3.id = 3
    setting_3.name = u"user_password"
    setting_3.value = u"123456"
    
    try:
        session.add(setting_3)
        session.flush()
        transaction.commit()
    except IntegrityError:
        transaction.abort()

    setting_4 = copy.deepcopy(setting_orig)

    setting_4.id = 4
    setting_4.name = u"mail_sender"
    setting_4.value = u"test1@gmail.com"
    
    try:
        session.add(setting_4)
        session.flush()
        transaction.commit()
    except IntegrityError:
        transaction.abort()
        
    setting_5 = copy.deepcopy(setting_orig)

    setting_5.id = 5
    setting_5.name = u"mail_smtppassword"
    setting_5.value = u"123456"
    
    try:
        session.add(setting_5)
        session.flush()
        transaction.commit()
    except IntegrityError:
        transaction.abort()

    setting_6 = copy.deepcopy(setting_orig)

    setting_6.id = 6
    setting_6.name = u"mail_template"
    setting_6.valuex = u"123456"
    
    try:
        session.add(setting_6)
        session.flush()
        transaction.commit()
    except IntegrityError:
        transaction.abort()
