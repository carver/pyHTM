'''
Created on Jan 31, 2011

@author: Jason
'''
import unittest
from carver.htm.io.translate_input import TranslateInput
import copy

class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testShiftXUp(self):
        a = [[1,2,3],[4,5,6],[7,8,9]]
        ti = TranslateInput(a, shift=[1,0], steps=2)
        
        iterator = iter(ti.dataGenerator())
        next = iterator.next()
        self.assertEqual(next, a)
        next = iterator.next()
        self.assertEqual(next, [[7,8,9],[1,2,3],[4,5,6]])
        next = iterator.next()
        self.assertEqual(next, [[4,5,6],[7,8,9],[1,2,3]])
        self.assertRaises(StopIteration, iterator.next)
        
    def testShiftXDown(self):
        a = [[1,2,3],[4,5,6],[7,8,9]]
        ti = TranslateInput(a, shift=[-1,0], steps=2)
        
        iterator = iter(ti.dataGenerator())
        next = iterator.next()
        self.assertEqual(next, a)
        next = iterator.next()
        self.assertEqual(next, [[4,5,6],[7,8,9],[1,2,3]])
        next = iterator.next()
        self.assertEqual(next, [[7,8,9],[1,2,3],[4,5,6]])
        self.assertRaises(StopIteration, iterator.next)
        
    def testShiftYUp(self):
        a = [[1,2,3],[4,5,6],[7,8,9]]
        ti = TranslateInput(a, shift=[0,1], steps=2)
        
        iterator = iter(ti.dataGenerator())
        next = iterator.next()
        self.assertEqual(next, a)
        next = iterator.next()
        self.assertEqual(next, [[3,1,2],[6,4,5],[9,7,8]])
        next = iterator.next()
        self.assertEqual(next, [[2,3,1],[5,6,4],[8,9,7]])
        self.assertRaises(StopIteration, iterator.next)
        
    def testShiftYDown(self):
        a = [[1,2,3],[4,5,6],[7,8,9]]
        ti = TranslateInput(a, shift=[0,-1], steps=2)
        
        iterator = iter(ti.dataGenerator())
        next = iterator.next()
        self.assertEqual(next, a)
        next = iterator.next()
        self.assertEqual(next, [[2,3,1],[5,6,4],[8,9,7]])
        next = iterator.next()
        self.assertEqual(next, [[3,1,2],[6,4,5],[9,7,8]])
        self.assertRaises(StopIteration, iterator.next)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testFlashCards']
    unittest.main()