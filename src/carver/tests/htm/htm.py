'''
Created on Dec 7, 2010

@author: Jason Carver
'''
import unittest
from carver.htm import HTM
from carver.htm.config import config


class TestHTM(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testInit(self):
        htm = HTM()
        data = [[1,0,1],[0,0,1]] #2d format, same dimensions as htm (for now)
        htm.initializeInput(data)
        self.assertEqual(htm.width, 2)
        self.assertEqual(htm.length, 3)
        cols = 0
        for col in htm.columns:
            cols += 1
            self.assertEqual(len(col.synapses), config.getint('init', 'synapses_per_segment'))
            
        self.assertEqual(cols, 6)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testInit']
    unittest.main()
