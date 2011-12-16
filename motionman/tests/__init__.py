import logging
import unittest

from pyramid import testing
from pyramid.config import Configurator

log = logging.getLogger(__name__)

__all__ = ['session', 'TestBase']

from sqlalchemy import create_engine
from motionman.models import initialize_sql
initialize_sql(create_engine('sqlite://'))
from motionman.models.init_data import init_data
init_data()

class TestBase(unittest.TestCase):
            
    def setUp(self):
        self.config = testing.setUp()
        self.request = testing.DummyRequest()
        log.info(self._testMethodName + " start...")
        
    def tearDown(self):
        testing.tearDown()
        log.info(self._testMethodName + " end...")

