'''
Created on Jan 31, 2011

@author: Jason
'''
import unittest
from carver.htm.io.flashcards import FlashCards


class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testFlashCards(self):
        mat1 = [[1,0,0],[0,1,1]]
        mat2 = [[1,0,1],[0,1,0]]
        mat3 = [[0,1,1],[1,0,0]]
        swap = FlashCards(3, mat1, mat2, mat3)
        
        data = [[0,0,0],[0,0,0]]
        swap.updateMatrix(data)
        self.assertEqual(data, mat1)
        swap.updateMatrix(data)
        self.assertEqual(data, mat1)
        swap.updateMatrix(data)
        self.assertEqual(data, mat1)
        swap.updateMatrix(data)
        self.assertEqual(data, mat2)
        swap.updateMatrix(data)
        self.assertEqual(data, mat2)
        swap.updateMatrix(data)
        self.assertEqual(data, mat2)
        swap.updateMatrix(data)
        self.assertEqual(data, mat3)
        swap.updateMatrix(data)
        self.assertEqual(data, mat3)
        swap.updateMatrix(data)
        self.assertEqual(data, mat3)
        swap.updateMatrix(data)
        self.assertEqual(data, mat1)
        swap.updateMatrix(data)
        self.assertEqual(data, mat1)
        swap.updateMatrix(data)
        self.assertEqual(data, mat1)
        swap.updateMatrix(data)
        self.assertEqual(data, mat2)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testFlashCards']
    unittest.main()