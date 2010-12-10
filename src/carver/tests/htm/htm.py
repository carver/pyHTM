'''
Created on Dec 7, 2010

@author: Jason Carver
'''
import unittest
from carver.htm import HTM
from carver.htm.config import config
from numenta.htm import pool_spatial, pool_temporal


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
        
    def flipDataGenerator(self, htm):
        def flipData(data):
            #flip all data
            for x in xrange(htm.width):
                for y in xrange(htm.length):
                    data[x][y] = not data[x][y]
        return flipData
        
    def testDataLoop(self):
        htm = self.htm
        data = [[1,0,1],[0,0,1]] #2d format, same dimensions as htm (for now)
    
        htm.initialize_input(data)
                    
        htm.execute(data, self.flipDataGenerator(htm), ticks=20)

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
                    
        flipDat = self.flipDataGenerator(htm)
        htm.execute(data, flipDat, ticks=50)
        active = htm.columns_active()
        htm.execute(data, flipDat, ticks=2)
        self.assertEqual(active, htm.columns_active())
        htm.execute(data, flipDat, ticks=2)
        self.assertEqual(active, htm.columns_active())
        
        #show that stability is non-trivial because it changes at the next time step
        htm.execute(data, flipDat)
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
                    
        flipDat = self.flipDataGenerator(htm)
        htm.execute(data, flipDat, ticks=100)
        
        htm.execute(data, flipDat, ticks=1)
        
        activeCols = htm.columns_active()
        
        #all columns should have learned particular cell patterns by now
        for col in activeCols:
            self.assertNotEqual(len(col.cells), len(filter(lambda cell: cell.active, col.cells)))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testInit']
    unittest.main()
