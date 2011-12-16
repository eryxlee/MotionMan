'''
Created on Aug 28, 2011

@author: eryx.lee
'''
import copy
import datetime
import transaction

from motionman.tests import TestBase
from motionman.models import DBSession

class TestModels(TestBase):
    def setUp(self):
        TestBase.setUp(self)

    def tearDown(self):
        TestBase.tearDown(self)

    def test_user_model(self):
        from motionman.models import User

        user_orig = User()
        user_orig.id = 888
        user_orig.email = u"test1@gmail.com"
        user_orig.name = u"test1"
        user_orig.vote_weight = 1
        user_orig.created_time = datetime.datetime.now()
        user_orig.created_user = 3
        user_orig.last_modified_time = datetime.datetime.now()
        user_orig.last_modified_user = 3
        user_orig.status = 2
        
        user_new = copy.deepcopy(user_orig)

        session = DBSession()
        session.add(user_new)
        session.flush()
        transaction.commit()

        user_load = session.query(User).filter(User.id==888).first()
        
        self.assertEqual(user_load.email, user_orig.email)
        self.assertEqual(user_load.name, user_orig.name)
        self.assertEqual(user_load.vote_weight, user_orig.vote_weight)
        self.assertEqual(user_load.created_time, user_orig.created_time)
        self.assertEqual(user_load.created_user, user_orig.created_user)
        self.assertEqual(user_load.last_modified_time, user_orig.last_modified_time)
        self.assertEqual(user_load.last_modified_user, user_orig.last_modified_user)
        self.assertEqual(user_load.status, user_orig.status)
        
        session.delete(user_load)
        session.flush()
        transaction.commit()            

    def test_setting_model(self):
        from motionman.models import Setting

        setting_orig = Setting()
        setting_orig.id = 888
        setting_orig.name = u"setting1"
        setting_orig.value = u"setting value"
        setting_orig.valuex = u"long setting value"
        setting_orig.created_time = datetime.datetime.now()
        setting_orig.created_user = 3
        setting_orig.last_modified_time = datetime.datetime.now()
        setting_orig.last_modified_user = 3
        setting_orig.status = 2
        
        setting_new = copy.deepcopy(setting_orig)

        session = DBSession()
        session.add(setting_new)
        session.flush()
        transaction.commit()

        setting_load = session.query(Setting).filter(Setting.id==888).first()
        
        self.assertEqual(setting_load.name, setting_orig.name)
        self.assertEqual(setting_load.value, setting_orig.value)
        self.assertEqual(setting_load.valuex, setting_orig.valuex)
        self.assertEqual(setting_load.created_time, setting_orig.created_time)
        self.assertEqual(setting_load.created_user, setting_orig.created_user)
        self.assertEqual(setting_load.last_modified_time, setting_orig.last_modified_time)
        self.assertEqual(setting_load.last_modified_user, setting_orig.last_modified_user)
        self.assertEqual(setting_load.status, setting_orig.status)
        
        session.delete(setting_load)
        session.flush()
        transaction.commit()            
