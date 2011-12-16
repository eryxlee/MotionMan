'''
Created on 2011-9-22

@author: eryxlee
'''
from motionman.tests import TestBase 

class Parent():
    def __init__(self):
        self.test = "from standard init"
        
    def init(self):
        self.test = "from init"

class Child(Parent):
    def __init__(self):
        Parent.__init__(self)
        
    def init(self):
        Parent.init(self)
        
def fake_init1(obj):
    obj.test = "from fake init1"

def fake_init2(obj):
    obj.test = "from fake init2"

class TestFirst(TestBase):
    def setUp(self):
        TestBase.setUp(self)

    def tearDown(self):
        TestBase.tearDown(self)

    def test_child(self):
        ch = Child()
        self.assertEqual(ch.test, "from standard init")
        ch.init()
        self.assertEqual(ch.test, "from init")

    def test_faked_child1(self):
        bak = Parent.__init__
        Parent.__init__ = fake_init1
        ch = Child()
        self.assertEqual(ch.test, "from fake init1")
        ch.init()
        self.assertEqual(ch.test, "from init")
        Parent.__init__ = bak

    def test_faked_child2(self):
        Parent.init = fake_init2
        ch = Child()
        self.assertEqual(ch.test, "from standard init")
        bak = Parent.init
        ch.init()
        self.assertEqual(ch.test, "from fake init2")
        Parent.init = bak