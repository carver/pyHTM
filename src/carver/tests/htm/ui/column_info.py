'''
Created on Feb 7, 2011

@author: Jason
'''
import unittest
from carver.htm import HTM
from carver.htm.io.flashcards import FlashCards
from carver.htm.ui.column_info import ColumnInfo


class ColumnInfoTest(unittest.TestCase):


    def setUp(self):
        mat1 = [[1,0,0],[0,1,1]]
        mat2 = [[1,0,1],[0,1,0]]
        mat3 = [[0,1,1],[1,0,0]]
        self.matrices = [mat1, mat2, mat3]
        cards = FlashCards(1, mat1, mat2, mat3)
        htm = HTM()
        htm.initialize_input(mat1)
        htm.execute(dataGenerator=cards.dataGenerator(), ticks=3*10, learning=True)
        
        self.htm = htm

    def tearDown(self):
        pass


    def testSynapseReport(self):
        htm = self.htm
        first = htm.columns.next()
        colInfo = ColumnInfo(first)
        print colInfo.legend()
        print colInfo.synapseTargets()
        
        htm.executeOnce(self.matrices[0], learning=False)
        states1 = colInfo.synapseStates()
        
        htm.executeOnce(self.matrices[1], learning=False)
        states2 = colInfo.synapseStates()
        
        htm.executeOnce(self.matrices[2], learning=False)
        states3 = colInfo.synapseStates()
        
        print states1
        print states2
        print states3
        
        self.assertNotEqual(states1, states2)
        self.assertNotEqual(states2, states3)
        self.assertNotEqual(states1, states3)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testSynapseReport']
    unittest.main()