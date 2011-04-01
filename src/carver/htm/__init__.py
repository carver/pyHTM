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
from carver.htm.synapse import SynapseState
from carver.htm.segment import Segment

INPUT_BIAS_PEAK = config.getfloat('init','input_bias_peak')
INPUT_BIAS_STD_DEV = config.getfloat('init','input_bias_std_dev')
EXTENSION_NEXT_STEP_PENALTY = config.getboolean('extensions', 'next_step_penalty')

class HTM(object):
    
    dimensions = 2 #hard-coded for now
    
    def __init__(self, cellsPerColumn=None):
        self.inhibitionRadius = config.getint('init', 'inhibitionRadius')
        
        impliedSparsity = float(config.getint('constants','desiredLocalActivity'))/(self.inhibitionRadius**self.dimensions)
        self.impliedSparsity = min(impliedSparsity, 1.0)
        
        if cellsPerColumn:
            self.cellsPerColumn = cellsPerColumn
        else:
            self.cellsPerColumn = config.getint('init','cells_per_column')
            
        self._inputCells = [[]] #a 2-d map of cells monitoring input
        self._updateSegments = UpdateSegments()
        
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
            #TODO: investigate why the magic number was 45, and how it changes with constants
            logging.warning('Increase the size of your input to at least 45 pixels or reduce your compression.\nDue to the segment activation threshold for prediction, too small a number of inputs prevents the HTM from learning temporal patterns')
        
        self.__wireColumnsToInput(self._data, inputWidth, inputLength)
                
        #add synapses on sequential/distal dendrites from each cell to cell,
        #which is not based on any known HTM docs
        #Actually, just let the first synapses grow on their own in temporal 1
        
    @property
    def inputWidth(self):
        return len(self._inputCells)
        
    @property
    def inputLength(self):
        return len(self._inputCells[0])
        
    def imagineNext(self):
        'project down estimates for next time step to the input cells, and step through'
        self._imagineStimulate(self.columns)
        self._imagineOverride(self._inputCells)
        self.__executeOne(False)
        
    @classmethod
    def stimulateFromColumns(cls, columns, columnFilter):
        for col in columns:
            if columnFilter(col):
                permanences = map(lambda syn: syn.permanence, col.synapsesConnected)
                down_scale = float(sum(permanences))
                
                for synapse in col.synapsesConnected:
                    synapse.input.stimulate(synapse.permanence / down_scale)
    
    @classmethod
    def _imagineStimulate(cls, columns):
        'testable step one of imagineNext'
        cls.stimulateFromColumns(columns, lambda col: col.predictingNext)
                    
    @classmethod
    def _imagineOverride(cls, inputCells):
        'testable step two of imagineNext'
                
        cls.normalize_input_stimulation(inputCells)
        
        for row in inputCells:
            for cell in row:
                cell.override()
        
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
        
        self._updateSegments = pool_temporal(self, self._updateSegments, learning=learning)
        
        #non-Numenta optimization:
        #track whether cell is predicted next
        #penalize near segments for failing immediately
        if EXTENSION_NEXT_STEP_PENALTY:
            for cell in self.cells:
                #mark prediction of immediate next step
                cell.predictingNext = False
                for segment in cell.segmentsNear:
                    if segment.active:
                        cell.predictingNext = True
                    
                if cell.predictedNext and not cell.active:
                    #penalize only active near segments
                    otherSynapseStates = []
                    for synapses in self._updateSegments[cell]:
                        if len(synapses) and synapses[0].segment == segment:
                            Segment.adapt_down(synapses)
                        else:
                            otherSynapseStates.append(synapses)
                            
                    self._updateSegments.reset(cell)
                    self._updateSegments.addAll(cell, otherSynapseStates)
        
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
                radius = ((c.x-syn.input.x)**2 + (c.y-syn.input.y)**2)**0.5
                if radius!=0:
                    radii.append(radius)
        return sum(radii)/len(radii)
    
    @classmethod
    def _max_input_stimulation(cls, inputCells):
        return max(cell.stimulation for row in inputCells for cell in row)
    
    @classmethod
    def normalize_input_stimulation(cls, inputCells):
        maxStim = cls._max_input_stimulation(inputCells)
        if maxStim:
            for row in inputCells:
                for cell in row:
                    cell.stimulation /= maxStim

class UpdateSegments(DictDefault):
    
    def __init__(self):
        DictDefault.__init__(self, newValueFunc=list)
        
    def add(self, cell, segment, timeDelta=0):
        '''
        @param timeDelta: when capturing state, do you capture current or previous state?
            current = 0; previous = -1
        '''
        states = SynapseState.captureSegmentState(segment, timeDelta)
        self[cell].append(states)
        
    def reset(self, cell):
        self[cell] = []
        
    def addAll(self, cell, segmentStates):
        self[cell].extend(segmentStates)
