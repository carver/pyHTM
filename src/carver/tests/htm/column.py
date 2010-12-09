'''
Created on Dec 7, 2010

@author: Jason Carver
'''
import unittest
from mock import Mock
from carver.htm.column import Column
from carver.htm import HTM


class TestColumn(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testSynapsesFiring(self):
        col = Column(HTM(), 0, 0, 4)
        
        firing = Mock({'is_firing':True})
        off = Mock({'is_firing':False})
        for i in xrange(4): #@UnusedVariable
            col.segment.add_synapse(firing)
            
        self.assertEqual(4, len(col.synapses_firing()))
        col.segment.add_synapse(off)
        self.assertEqual(4, len(col.synapses_firing()))
        col.segment.add_synapse(firing)
        self.assertEqual(5, len(col.synapses_firing()))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testInit']
    unittest.main()
