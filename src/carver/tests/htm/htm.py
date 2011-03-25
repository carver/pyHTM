'''
Created on Dec 7, 2010

@author: Jason Carver
'''
import unittest
from carver.htm import HTM
from carver.htm.config import config
from htm_main import flipDataGenerator
from mock import Mock

class TestHTM(unittest.TestCase):


    def setUp(self):
        self.htm = HTM()
        self.data = [[1,0,1],[0,0,1]] #2d format, same dimensions as htm (for now)
        pass


    def tearDown(self):
        pass

    def _initialize(self):
        self.htm.initialize_input(self.data)

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
        
    def testDataLoop(self):
        htm = self.htm
        data = [[1,0,1],[0,0,1]] #2d format, same dimensions as htm (for now)
    
        htm.initialize_input(data)
                    
        htm.execute(flipDataGenerator(htm), ticks=20)

        #show output (this is way too verbose to leave in for long, 
        #    but useful during early testing)
#        for cell in htm.cells:
#            print cell
#        for col in htm.columns:
#            print col

    def testStability(self):
        'test that repeated patterns get recognized by the same columns after stabilizing'
        htm = self.htm
        
        #2d format, same dimensions as htm (for now)
        data = [[1,0,1,0,1,0,1,0,1,0],[0,0,0,0,1,0,0,0,0,1]]
        
        htm.initialize_input(data)
                    
        flipDat = flipDataGenerator(htm)
        htm.execute(flipDat, ticks=50)
        active = htm.columns_active()
        htm.execute(flipDat, ticks=1)
        self.assertEqual(active, htm.columns_active())
        htm.execute(flipDat, ticks=1)
        self.assertEqual(active, htm.columns_active())
        
        #show that stability is non-trivial because it changes at the next time step
        htm.execute(flipDat, ticks=0)
        self.assertNotEqual(active, htm.columns_active())

    def testPatternTraining(self):
        'test that within columns, particular cells dominate when they recognize learned temporal patterns'
        htm = self.htm
        
        #2d format, same dimensions as htm (for now)
        data = [
            [1,0,1,0,1,0,1,0,1,0],
            [0,0,0,0,1,0,1,0,1,1],
            [0,0,1,0,1,0,0,0,0,1],
            [0,1,0,0,1,1,0,1,0,1],
            [1,0,1,0,1,0,1,0,0,1],
            [0,0,0,1,1,0,0,0,1,1],
            ]
        
        htm.initialize_input(data)
                    
        flipDat = flipDataGenerator(htm)
        htm.execute(flipDat, ticks=100)
        
        activeCols = htm.columns_active()
        
        #all columns should have learned particular cell patterns by now
        for col in activeCols:
            self.assertNotEqual(len(col.cells), len(filter(lambda cell: cell.active, col.cells)))
            
    def testImagination(self):
        input1 = Mock()
        input1.stimulation=0
        input2 = Mock()
        input2.stimulation=0
        synapse1 = Mock()
        synapse1.input = input1
        synapse2 = Mock()
        synapse2.input = input2
        col1 = Mock()
        col1.synapsesConnected = [synapse1, synapse2]
        col2 = Mock()
        col2.synapsesConnected = [synapse2]
        columns = [col1,col2]
        inputCells = [[input1, input2]]
        
        self.htm._imagineStimulate(columns)
        
        input1.mockCheckCall(0, 'stimulate', 0.5)
        input2.mockCheckCall(0, 'stimulate', 0.5)
        input2.mockCheckCall(1, 'stimulate', 1)
        
        #TODO test input cells stimulation and override
        input1.stimulation = 0.5
        input2.stimulation = 1.5
        
        self.htm._imagineOverride(inputCells)
        input1.mockCheckCall(1, 'override')
        input2.mockCheckCall(2, 'override')
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testInit']
    unittest.main()
