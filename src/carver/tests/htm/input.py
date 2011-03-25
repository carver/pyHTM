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
        
    def testStimulate(self):
        data = [[0,0,0], [0,0,0]]
        cell = InputCell(0, 0, data)
        cell.stimulate(.5)
        self.assertEqual(0.5, cell.stimulation)
        cell.stimulate(2.5)
        cell.stimulation /= 2
        self.assertEqual(1.5, cell.stimulation)
        
        self.assertFalse(cell.wasActive)
        cell.override()
        self.assertEqual(0, cell.stimulation)
        self.assert_(cell.wasActive)
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testInit']
    unittest.main()
