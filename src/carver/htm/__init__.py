'''
Created on Dec 7, 2010

@author: Jason Carver

Numenta docs are (c) Numenta
'''
from carver.htm import column
from carver.htm import synapse
from carver.htm.config import config
from carver.htm import segment
from carver.htm import input
import random
from math import exp, sqrt

INPUT_BIAS_PEAK = config.getfloat('init','input_bias_peak')
INPUT_BIAS_STD_DEV = config.getfloat('init','input_bias_std_dev')

class HTM(object):
    def __init__(self):
        self.inhibitionRadius = config.getint('init', 'inhibitionRadius')
        self.cellsPerColumn = config.getint('init','cells_per_column')
        
    @property
    def columns(self):
        for x in xrange(self.width):
            for y in xrange(self.length):
                yield self._column_grid[x][y]
                
    @property
    def columnsActive(self):
        return filter(lambda c: c.active, self.columns)
    
    def __createColumns(self, width, length):
        #columns is a 2d list of lists, where x and y should line up with indices
        self._column_grid = []
        for x in xrange(width):
            columnsInX = []
            for y in xrange(length):
                columnsInX.append(column.Column(self, x, y, self.cellsPerColumn))
            self._column_grid.append(columnsInX)
        
        self.width = width
        self.length = length
        
    def initializeInput(self, data):
        '''assume 2d for now
        Inspired by HTM doc 0.1.1, pg 34
        '''
        
        inputWidth = len(data)
        inputLength = len(data[0])
        self.__createColumns(inputWidth, inputLength)
        
        self.__wireColumnsToInput(data, inputWidth, inputLength)
                
        #add synapses on sequential/distal dendrites from each cell to cell,
        #which is not based on any known HTM docs
        #Actually, just let the first synapses grow on their own in temporal 1
        
    def __wireColumnsToInput(self, data, inputWidth, inputLength):
        longerSide = max(inputWidth, inputLength)
        cellProxies = [[input.InputCell(x, y, data) for y in xrange(inputLength)] for x in xrange(inputWidth)]
        
        #give starting permanence value near the threshold
        #bias permanence up toward column center as a gaussian distribution
        for col in self.columns:
            for i in xrange(synapse.SYNAPSES_PER_SEGMENT):
                inputx = random.randint(0,inputWidth-1)
                inputy = random.randint(0,inputLength-1)
                cellProxy = cellProxies[inputx][inputy]
                rand_permanence = random.gauss(synapse.CONNECTED_CUTOFF, 
                    synapse.PERMANENCE_INCREMENT*2)
                distance = col.distance_to(inputx, inputy)
                locality_bias = (INPUT_BIAS_PEAK/0.4)*exp((distance/(longerSide*INPUT_BIAS_STD_DEV))**2/-2)
                syn = synapse.Synapse(cellProxy, permanence=rand_permanence*locality_bias)
                col.segment.add_synapse(syn)
    
    def __radiusUp(self, val, edge):
        return min(edge, max(val+1, int(round(val + self.inhibitionRadius))))
    def __radiusDown(self, val, edge):
        return max(0, min(val-1, int(round(val - self.inhibitionRadius))))
    
    def neighbors(self, column):
        #boundries
        startx = self.__radiusDown(column.x, 0)
        starty = self.__radiusDown(column.y, 0)
        endx = self.__radiusUp(column.x, self.width)
        endy = self.__radiusUp(column.y, self.length)
        
        for x in xrange(startx, endx):
            for y in xrange(starty, endy):
                yield self._column_grid[x][y]
                
    @property
    def cells(self):
        for col in self.columns:
            for cell in col.cells:
                yield cell
                
    def average_receptive_field_size(self):
        '''
        Numenta docs:
        The radius of the average connected receptive field size of all the columns. 
        The connected receptive field size of a column includes only the connected 
        synapses (those with permanence values >= connectedPerm).  This is used 
        to determine the extent of lateral inhibition between columns. 
        '''
        radii = []
        for c in self.columns:
            for syn in c.synapsesConnected:
                radii.append(((c.x-syn.input.x)**2 + (c.y-syn.input.y)**2)**0.5)
        return sum(radii)/len(radii)
