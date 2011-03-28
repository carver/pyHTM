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
import logging
from math import exp, sqrt
from copy import deepcopy
from carver.utilities.dict_default import DictDefault

INPUT_BIAS_PEAK = config.getfloat('init','input_bias_peak')
INPUT_BIAS_STD_DEV = config.getfloat('init','input_bias_std_dev')

class HTM(object):
    def __init__(self, cellsPerColumn=None):
        self.inhibitionRadius = config.getint('init', 'inhibitionRadius')
        if cellsPerColumn:
            self.cellsPerColumn = cellsPerColumn
        else:
            self.cellsPerColumn = config.getint('init','cells_per_column')
            
        self._inputCells = [[]] #a 2-d map of cells monitoring input
        self._updateSegments = DictDefault(list)
        
    @property
    def columns(self):
        for x in xrange(self.width):
            for y in xrange(self.length):
                yield self._column_grid[x][y]
             
    def columns_active(self):
        return filter(lambda c: c.active, self.columns)
    
    def __createColumns(self, inputWidth, inputLength, inputCompression):
        '''
        @param inputWidth: width of input cells
        @param inputLength: length of input cells
        @param inputCompression: ratio of input cells to columns
        '''
        #columns is a 2d list of lists, where x and y should line up with indices
        self._column_grid = []
        
        width = int(inputWidth / inputCompression)
        length = int(inputLength / inputCompression)
        
        for x in xrange(width):
            columnsInX = []
            for y in xrange(length):
                columnsInX.append(column.Column(self, x, y, self.cellsPerColumn))
            self._column_grid.append(columnsInX)
        
        return (width, length)
        
    def initialize_input(self, data, compressionFactor=1.0):
        '''
        assume 2d for now
        Inspired by HTM doc 0.1.1, pg 34
        @param data: an example matrix of data
        @param compressionFactor: the ratio of input pixels to columns
        '''
        self._data = deepcopy(data)
        self.inputCompression = compressionFactor
        
        inputWidth = len(data)
        inputLength = len(data[0])
        
        (self.width, self.length) = self.__createColumns(
            inputWidth, inputLength, self.inputCompression)
        
        if self.width * self.length < 45:
            logging.warning('Increase the size of your input to at least 45 pixels or reduce your compression.\nDue to the segment activation threshold for prediction, too small a number of inputs prevents the HTM from learning temporal patterns')
        
        self.__wireColumnsToInput(self._data, inputWidth, inputLength)
                
        #add synapses on sequential/distal dendrites from each cell to cell,
        #which is not based on any known HTM docs
        #Actually, just let the first synapses grow on their own in temporal 1
        
    def imagineNext(self):
        'project down estimates for next time step to the input cells, and step through'
        self._imagineStimulate(self.columns)
        self._imagineOverride(self._inputCells)
        self.__executeOne(False)
    
    @classmethod
    def _imagineStimulate(cls, columns):
        'testable step one of imagineNext'
        for col in columns:
            if col.predictingNext:
                down_scale = len(col.synapsesConnected)
                activityPerSynapse = float(1) / down_scale
                
                for synapse in col.synapsesConnected:
                    synapse.input.stimulate(activityPerSynapse)
                    
    @classmethod
    def _imagineOverride(cls, inputCells):
        'testable step two of imagineNext'
                
        #flatten cell matrix
        allInputs = []
        for row in inputCells:
            for cell in row:
                allInputs.append(cell)
                
        maxStim = max(map(lambda inCell: inCell.stimulation, allInputs))
        if maxStim:
            for inCell in allInputs:
                inCell.stimulation /= maxStim
                inCell.override()
        
    def executeOnce(self, data, learning=True, postTick=None):
        '''
        @param data: current input data
        '''
        self.updateMatrix(data)
        self.__executeOne(learning)
        if postTick:
            postTick(self)
        
    def execute(self, dataGenerator, ticks=None, learning=True,
        postTick=None):
        '''
        execute htm pooling across time
        @param dataGenerator: generates next input data at each time step, 
            iter(dataGenerator) must produce a valid iterator
        @param ticks: how many iterations of execution to run
        @param learning: whether the htm executes in learning mode
        @param postTick: call this function after every iteration,
            with the htm as an argument
        '''
        
        for data in iter(dataGenerator):
            self.executeOnce(data, learning, postTick)
                
            if ticks is not None:
                ticks -= 1
                if ticks < 0:
                    break
        
    def __executeOne(self, learning):
        from numenta.htm import pool_spatial, pool_temporal
        
        for cell in self.cells:
                cell.clockTick()
                
        pool_spatial(self)
        
        self._updateSegments = pool_temporal(self, self._updateSegments, learning=True)
        
    def updateMatrix(self, newData):
        for x in xrange(len(newData)):
            for y in xrange(len(newData[x])):
                self._data[x][y] = newData[x][y]
        
    def __wireColumnsToInput(self, data, inputWidth, inputLength):
        longerSide = max(inputWidth, inputLength)
        cellProxies = [[input.InputCell(x, y, data) for y in xrange(inputLength)] for x in xrange(inputWidth)]
        
        self._inputCells = cellProxies
        
        #give starting permanence value near the threshold
        #bias permanence up toward column center as a gaussian distribution
        for col in self.columns:
            for _i in xrange(synapse.SYNAPSES_PER_SEGMENT):
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
