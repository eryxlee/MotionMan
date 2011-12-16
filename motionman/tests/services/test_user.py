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
from motionman.models import User

class TestUser(TestBase):
    def setUp(self):
        TestBase.setUp(self)

        self.user_orig = User()
        self.user_orig.email = u""
        self.user_orig.name = u"test1"
        self.user_orig.vote_weight = 1
        self.user_orig.created_time = datetime.datetime.now()
        self.user_orig.created_user = 0
        self.user_orig.last_modified_time = datetime.datetime.now()
        self.user_orig.last_modified_user = 0
        self.user_orig.status = 1
        
    def tearDown(self):
        TestBase.tearDown(self)
        
    def test_load_users(self):
        from motionman.services.user import load_users
        
        #prepare data
        session = DBSession()

        user_1 = copy.deepcopy(self.user_orig)

        try:
            session.add(user_1)
            session.flush()
            transaction.commit()
        except IntegrityError:
            transaction.abort()
        
        user_2 = copy.deepcopy(self.user_orig)
        user_2.name = u"test2"
        try:
            session.add(user_2)
            session.flush()
            transaction.commit()
        except IntegrityError:
            transaction.abort()
        
        user_3 = copy.deepcopy(self.user_orig)
        user_3.name = u"test3"
        user_3.status = 0
        try:
            session.add(user_3)
            session.flush()
            transaction.commit()
        except IntegrityError:
            transaction.abort()

        users = load_users()
        user1_found = False
        user2_found = False
        user3_found = False
        for user in users:
            if user.name == u'test1': user1_found = True
            if user.name == u'test2': user2_found = True
            if user.name == u'test3': user3_found = True
        
        self.assertTrue(user1_found)
        self.assertTrue(user2_found)
        self.assertFalse(user3_found)

    def test_load_user(self):
        from motionman.services.user import load_user
        session = DBSession()
        
        user_1 = copy.deepcopy(self.user_orig)

        user_1.email = u"testemail"
        user_1.name = u"testname"
        user_1.vote_weight = 88
        try:
            session.add(user_1)
            session.flush()
        except IntegrityError:
            transaction.abort()
        
        user_load = load_user(user_1.id)
        
        self.assertEqual(user_load.name, u'testname')
        self.assertEqual(user_load.email, u'testemail')
        self.assertEqual(user_load.vote_weight, 88)
        self.assertEqual(user_load.status, 1)
        
        session.delete(user_load)
        session.flush()
        transaction.commit()

        
    def test_add_user(self):
        from motionman.services.user import add_user, DuplicatedName, DuplicatedEmail
        add_user(u"testname", u"testemail", 88)
        
        session = DBSession()
        user_load = session.query(User).filter(User.name==u'testname').first()
        
        self.assertEqual(user_load.name, u'testname')
        self.assertEqual(user_load.email, u'testemail')
        self.assertEqual(user_load.vote_weight, 88)
        self.assertEqual(user_load.status, 1)
        
        self.assertRaises(DuplicatedName, add_user, u"testname", u"different email", 88)
        self.assertRaises(DuplicatedEmail, add_user, u"different name", u"testemail", 88)
        
        session.delete(user_load)
        session.flush()
        transaction.commit()

    def test_update_user(self):
        from motionman.services.user import update_user
        
        #prepare data
        session = DBSession()

        user_1 = copy.deepcopy(self.user_orig)

        try:
            session.add(user_1)
            session.flush()
        except IntegrityError:
            transaction.abort()
        
        update_user(user_1.id, u'newname', u'newemail', 888)

        user_load = session.query(User).filter(User.id==user_1.id).first()
        self.assertEqual(user_load.name, u'newname')
        self.assertEqual(user_load.email, u'newemail')
        self.assertEqual(user_load.vote_weight, 888)
        self.assertEqual(user_load.status, 1)
        
        session.delete(user_load)
        session.flush()
        transaction.commit()


    def test_delete_user(self):
        from motionman.services.user import delete_user
        from sqlalchemy import and_
        
        #prepare data
        session = DBSession()

        user_1 = copy.deepcopy(self.user_orig)

        try:
            session.add(user_1)
            session.flush()
        except IntegrityError:
            transaction.abort()
        
        delete_user(user_1.id)

        user_load = session.query(User).filter(and_(User.id==user_1.id, User.status==1)).first()
        self.assertEqual(user_load, None)

        user_load = session.query(User).filter(User.id==user_1.id).first()
        self.assertEqual(user_load.status, 0)
