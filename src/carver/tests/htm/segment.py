'''
Created on Dec 7, 2010

@author: Jason Carver
'''
import unittest
from carver.htm.synapse import Synapse, CONNECTED_CUTOFF
from mock import Mock
from carver.htm.input import InputCell
from carver.htm.segment import Segment, FRACTION_SEGMENT_ACTIVATION_THRESHOLD
#from carver.htm.config import config


class TestSegment(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass

    def testAggregation(self):
        seg = Segment()
        self.assertFalse(seg.active)
        
        firing = Mock({'is_firing':True})
        off = Mock({'is_firing':False})
        
        seg.add_synapse(off)
        self.assertFalse(seg.active)
        
        onRequired = int(FRACTION_SEGMENT_ACTIVATION_THRESHOLD*100)
        offRequired = 99-onRequired
        
        #this isn't a hard requirement, just a limitation of the test
        assert(onRequired >= 2)
        
        for _ in xrange(offRequired):
            seg.add_synapse(off)
            
        self.assertFalse(seg.active)
        
        for _ in xrange(onRequired-1):
            seg.add_synapse(firing)
        
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
