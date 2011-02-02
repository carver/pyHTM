'''
Created on Feb 1, 2011

@author: Jason
'''
import unittest
from carver.htm.io.objectrecognize import ObjectRecognize


class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testDataMatrix(self):
        names = ['a','b','c']
        data = [[2,0,0],[0,2,0],[0,0,2]]
        obrec = ObjectRecognize()
        obrec.label('a', data[0])
        obrec.label('b', data[1])
        obrec.label('c', data[2])
        data = [[2,0,0],[2,2,0],[1,0,2]]
        print obrec.getMatchText(names, data)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testDataMatrix']
    unittest.main()