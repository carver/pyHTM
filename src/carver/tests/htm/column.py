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
        self.col = Column(HTM(), 0, 0, 4)
        pass


    def tearDown(self):
        pass


    def testSynapsesFiring(self):
        col = self.col
        
        firing = Mock({'was_firing':True})
        off = Mock({'was_firing':False})
        for _ in xrange(4):
            col.segment.add_synapse(firing)
            
        self.assertEqual(4, len(col.old_firing_synapses()))
        col.segment.add_synapse(off)
        self.assertEqual(4, len(col.old_firing_synapses()))
        col.segment.add_synapse(firing)
        self.assertEqual(5, len(col.old_firing_synapses()))
        
    def testBestCell(self):
        #trivial case (no synapses explicitly set on any cells):
        self.assertNotEqual(None, self.col.bestCell())

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testInit']
    unittest.main()
