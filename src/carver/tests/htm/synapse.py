'''
Created on Dec 7, 2010

@author: Jason Carver
'''
import unittest
from carver.htm.synapse import Synapse, CONNECTED_CUTOFF
from mock import Mock
#from carver.htm.config import config


class TestSynapse(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testFiring(self):
        input = Mock()
        input.wasActive = True
        s = Synapse(input, permanence=CONNECTED_CUTOFF + 0.1)
        self.assert_(s.is_firing())
        self.assert_(s.is_firing(acrossSynapse=True))
        self.assert_(s.is_firing(acrossSynapse=False))
        
        input = Mock()
        input.wasActive = True
        s = Synapse(input, permanence=CONNECTED_CUTOFF - 0.1)
        self.assertFalse(s.is_firing())
        self.assertFalse(s.is_firing(acrossSynapse=True))
        self.assert_(s.is_firing(acrossSynapse=False))
        
        input = Mock()
        input.wasActive = False
        s = Synapse(input, permanence=CONNECTED_CUTOFF + 0.1)
        self.assertFalse(s.is_firing())
        self.assertFalse(s.is_firing(acrossSynapse=True))
        self.assertFalse(s.is_firing(acrossSynapse=False))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testInit']
    unittest.main()
