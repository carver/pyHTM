'''
Created on Dec 7, 2010

@author: Jason Carver
'''
import unittest
from carver.htm.synapse import Synapse, CONNECTED_CUTOFF
from mock import Mock
from carver.htm.input import InputCell
from carver.htm.segment import Segment, SEGMENT_ACTIVATION_THRESHOLD
#from carver.htm.config import config


class TestSegment(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass

    def testAggregation(self):
        seg = Segment()
        
        firing = Mock({'is_firing':True})
        off = Mock({'is_firing':False})
        for i in xrange(SEGMENT_ACTIVATION_THRESHOLD-1): #@UnusedVariable
            seg.add_synapse(firing)
            
        self.assertFalse(seg.active)
        seg.add_synapse(off)
        self.assertFalse(seg.active)
        seg.add_synapse(firing)
        self.assert_(seg.active)
        
    def testAdaptation(self):
        seg = Segment()
        
        #for now, just don't crash
        seg.adapt_up()
        seg.adapt_down()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testInit']
    unittest.main()
