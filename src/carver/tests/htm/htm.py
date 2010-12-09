'''
Created on Dec 7, 2010

@author: Jason Carver
'''
import unittest
from carver.htm import HTM
from carver.htm.config import config


class TestHTM(unittest.TestCase):


    def setUp(self):
        self.htm = HTM()
        self.data = [[1,0,1],[0,0,1]] #2d format, same dimensions as htm (for now)
        pass


    def tearDown(self):
        pass

    def _initialize(self):
        self.htm.initializeInput(self.data)

    def testInit(self):
        htm = self.htm
        
        self._initialize()
        self.assertEqual(htm.width, 2)
        self.assertEqual(htm.length, 3)
        cols = 0
        for col in htm.columns:
            cols += 1
            self.assertEqual(len(col.synapses), config.getint('init', 'synapses_per_segment'))
            
        self.assertEqual(cols, 6)
        
    def testKthNeighbor(self):
        'kth_neighbor in small networks'
        htm = self.htm
        self._initialize()
        
        sameNeighbor = None
        for col in htm.columns:
            neighbor = col.kth_neighbor(7) #ask for a lower neighbor than exists
            if sameNeighbor is not None:
                self.assertEqual(sameNeighbor, neighbor)
            else:
                sameNeighbor = neighbor
                
    def testReceptiveField(self):
        self._initialize()
        self.htm.average_receptive_field_size()
        
    def testDataFlow(self):
        self._initialize()
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testInit']
    unittest.main()
