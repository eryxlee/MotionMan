'''
Created on Aug 29, 2011

@author: eric
'''
import copy
import datetime
import transaction

from sqlalchemy.exc import IntegrityError

from motionman.tests import TestBase
from motionman.models import DBSession
from motionman.models import Setting


class TestSetting(TestBase):
    def setUp(self):
        TestBase.setUp(self)

        self.setting_orig = Setting()
        self.setting_orig.name = u"test1"
        self.setting_orig.value = u""
        self.setting_orig.valuex = u""
        self.setting_orig.created_time = datetime.datetime.now()
        self.setting_orig.created_user = 0
        self.setting_orig.last_modified_time = datetime.datetime.now()
        self.setting_orig.last_modified_user = 0
        self.setting_orig.status = 1
        
    def tearDown(self):
        TestBase.tearDown(self)
        
    def test_load_settings(self):
        from motionman.services.setting import load_settings
        
        #prepare data
        session = DBSession()

        setting_1 = copy.deepcopy(self.setting_orig)

        try:
            session.add(setting_1)
            session.flush()
            transaction.commit()
        except IntegrityError:
            transaction.abort()
        
        setting_2 = copy.deepcopy(self.setting_orig)
        setting_2.name = u"test2"
        try:
            session.add(setting_2)
            session.flush()
            transaction.commit()
        except IntegrityError:
            transaction.abort()
        
        setting_3 = copy.deepcopy(self.setting_orig)
        setting_3.name = u"test3"
        setting_3.status = 0
        try:
            session.add(setting_3)
            session.flush()
            transaction.commit()
        except IntegrityError:
            transaction.abort()

        settings = load_settings()
        test1_found = False
        test2_found = False
        test3_found = False
        for setting in settings:
            if setting.name == u'test1': test1_found = True
            if setting.name == u'test2': test2_found = True
            if setting.name == u'test3': test3_found = True
        
        self.assertTrue(test1_found)
        self.assertTrue(test2_found)
        self.assertFalse(test3_found)
        
    def test_update_setting(self):
        from motionman.services.setting import update_setting

        session = DBSession()

        setting_1 = copy.deepcopy(self.setting_orig)

        try:
            session.add(setting_1)
            session.flush()
        except IntegrityError:
            transaction.abort()
        
        session.refresh(setting_1)
        
        update_setting(setting_1.id, u"new value", u"new valuex")
        
        setting_load = session.query(Setting).filter(Setting.id==setting_1.id).first()
        
        self.assertEqual(setting_load.value, u"new value")
        self.assertEqual(setting_load.valuex, u"new valuex")
        
        #assert other records are not changed.

    def test_get_value_by_name(self):
        from motionman.services.setting import get_value_by_name, update_setting
        
        session = DBSession()

        setting_load = session.query(Setting).filter(Setting.name==u'motion_id_prefix').first()
        update_setting(setting_load.id, u"newtestofidprefix", u"newtestvaluexofidprefix")
        self.assertEqual(get_value_by_name(u'motion_id_prefix')[0], u"newtestofidprefix")
        self.assertEqual(get_value_by_name(u'motion_id_prefix')[1], u"newtestvaluexofidprefix")
        
        setting_load = get_value_by_name(u'srwerslf3sfsofdfs')
        self.assertEqual(setting_load, None)

    def test_get_config_by_name(self):
        from motionman.services.setting import get_config_by_name, update_setting, MissConfiguration
        
        session = DBSession()

        setting_load = session.query(Setting).filter(Setting.name==u'motion_id_prefix').first()
        update_setting(setting_load.id, u"newtestofidprefix", u"newtestvaluexofidprefix")
        self.assertEqual(get_config_by_name(u'motion_id_prefix')[0], u"newtestofidprefix")
        self.assertEqual(get_config_by_name(u'motion_id_prefix')[1], u"newtestvaluexofidprefix")
        
        self.assertRaises(MissConfiguration, get_config_by_name, u"srwerslf3sfsofdfs")
        
    def test_get_motion_id_prefix(self):
        from motionman.services.setting import get_motion_id_prefix, update_setting
        
        session = DBSession()

        setting_load = session.query(Setting).filter(Setting.name==u'motion_id_prefix').first()
        update_setting(setting_load.id, u"newtestofidprefix")
        self.assertEqual(get_motion_id_prefix(), u"newtestofidprefix")
    
    def test_get_admin_password(self):
        from motionman.services.setting import get_admin_password, update_setting

        session = DBSession()
        
        setting_load = session.query(Setting).filter(Setting.name==u'admin_password').first()
        update_setting(setting_load.id, u"newtestofadminpassword")
        self.assertEqual(get_admin_password(), u"newtestofadminpassword")

    
    def test_get_user_password(self):
        from motionman.services.setting import get_user_password, update_setting

        session = DBSession()
        
        setting_load = session.query(Setting).filter(Setting.name==u'user_password').first()
        update_setting(setting_load.id, u"newtestofuserpassword")
        self.assertEqual(get_user_password(), u"newtestofuserpassword")

    def test_get_mail_sender(self):
        from motionman.services.setting import get_mail_sender, update_setting

        session = DBSession()
        
        setting_load = session.query(Setting).filter(Setting.name==u'mail_sender').first()
        update_setting(setting_load.id, u"newtestofmailsender")
        self.assertEqual(get_mail_sender(), u"newtestofmailsender")

    def test_get_mail_smtppassword(self):
        from motionman.services.setting import get_mail_smtppassword, update_setting

        session = DBSession()
        
        setting_load = session.query(Setting).filter(Setting.name==u'mail_smtppassword').first()
        update_setting(setting_load.id, u"newtestofmailsmtppassword")
        self.assertEqual(get_mail_smtppassword(), u"newtestofmailsmtppassword")

    def test_get_mail_template(self):
        from motionman.services.setting import get_mail_template, update_setting

        session = DBSession()
        
        setting_load = session.query(Setting).filter(Setting.name==u'mail_template').first()
        update_setting(setting_load.id, u"", u"newtestofmailtemplate")
        self.assertEqual(get_mail_template(), u"newtestofmailtemplate")
        
