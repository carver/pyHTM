'''
Created on Dec 7, 2010

@author: Jason Carver
'''
import unittest
from carver.htm.synapse import Synapse, CONNECTED_CUTOFF
from mock import Mock
from carver.htm.input import InputCell
#from carver.htm.config import config


class TestInputCell(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass

    def testWasActive(self):
        data = [[1,1,0], [0,0,1]]
        cell = InputCell(0, 0, data)
        self.assert_(cell.wasActive)
        cell = InputCell(0, 1, data)
        self.assert_(cell.wasActive)
        cell = InputCell(0, 2, data)
        self.assertFalse(cell.wasActive)
        cell = InputCell(1, 0, data)
        self.assertFalse(cell.wasActive)
        cell = InputCell(1, 1, data)
        self.assertFalse(cell.wasActive)
        cell = InputCell(1, 2, data)
        self.assert_(cell.wasActive)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testInit']
    unittest.main()
