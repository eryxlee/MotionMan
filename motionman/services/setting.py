'''
Created on Aug 28, 2011

@author: eric
'''
import logging

from motionman.models import DBSession
from motionman.models import Setting

log = logging.getLogger(__name__)

class MissConfiguration(Exception):
    pass

def load_settings():
    session = DBSession()
    return session.query(Setting).filter(Setting.status==1).all()

def update_setting(name, value, valuex = None):
    session = DBSession()
    session.query(Setting).filter(Setting.name==name).update({Setting.value:value,Setting.valuex:valuex})
    
def get_value_by_name(name):
    session = DBSession()
    setting = session.query(Setting).filter(Setting.name==name).first()
    if setting:
        return (setting.value, setting.valuex)

def get_config_by_name(name):
    session = DBSession()
    setting = session.query(Setting).filter(Setting.name==name).first()
    if setting:
        return (setting.value, setting.valuex)
    else:
        log.error(u"Can't %s from configuration" % name)
        raise MissConfiguration()

def get_motion_id_prefix():
    return get_config_by_name(u"motion_id_prefix")[0]

def get_admin_password():
    return get_config_by_name(u"admin_password")[0]

def get_user_password():
    return get_config_by_name(u"user_password")[0]

def get_mail_sender():
    return get_config_by_name(u"mail_sender")[0]

def get_mail_smtppassword():
    return get_config_by_name(u"mail_smtppassword")[0]

def get_mail_template():
    return get_config_by_name(u"mail_template")[1]
