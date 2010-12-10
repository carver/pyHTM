'''
Created on Dec 7, 2010

@author: Jason Carver
'''
import unittest
from mock import Mock
from carver.htm.column import Column
from carver.htm import HTM
from carver.htm.cell import Cell
from carver.htm.config import config


class TestColumn(unittest.TestCase):


    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testCreateSegment(self):
        h = HTM()
        h.initialize_input([[1,1]])
        cell = Cell()
        startingSegments = config.getint('init','segments_per_cell')
        self.assertEqual(startingSegments, len(cell.segments))
        cell.create_segment(h)
        self.assertEqual(startingSegments+1, len(cell.segments))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testInit']
    unittest.main()
