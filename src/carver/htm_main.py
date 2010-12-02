'''
Created on Nov 26, 2010

@author: Jason Carver

Numenta docs are (c) Numenta
'''
from carver.htm.column import Column
from carver.htm.config import config
from numenta.htm import pool_spatial, pool_temporal

def kth_score(columns, k):
    '''
    Numenta docs: Given the list of columns, return the kth highest overlap value
    '''
    return sorted(columns, key=lambda col: col.overlap)[k-1]

def neighbor_duty_cycle_max(column):
    '''
    (Adapted from maxDutyCycle)
    Numenta docs: Returns the maximum active duty cycle of the columns in the 
    given list of colmns  
    '''
    return max((c.dutyCycleActive for c in column.neighbors))

def average_receptive_field_size(columns):
    '''
    Numenta docs:
    The radius of the average connected receptive field size of all the columns. 
    The connected receptive field size of a column includes only the connected 
    synapses (those with permanence values >= connectedPerm).  This is used 
    to determine the extent of lateral inhibition between columns. 
    '''
    radii = []
    for c in columns:
        for syn in c.synapsesConnected:
            radii.append(((c.x-syn.x)**2, (c.y-syn.y)**2)**0.5)
    return sum(radii)/len(radii)

def create_dendrite_segment(htm, cell):
    '''
    set to distal by default
    
    Adapted from getSegmentActiveSynapses() with newSynapses=True
    Numenta docs:
    Return a segmentUpdate data structure containing a list of proposed 
    changes to segment s. Let activeSynapses be the list of active synapses 
    where the originating cells have their activeState output = 1 at time step t.  
    (This list is empty if s = -1 since the segment doesn't exist.) newSynapses 
    is an optional argument that defaults to false. If newSynapses is true, then 
    newSynapseCount - count(activeSynapses) synapses are added to 
    activeSynapses. These synapses are randomly chosen from the set of cells 
    that have learnState output = 1 at time step t. 
    This function iterates through a list of segmentUpdate's and reinforces 
    '''
    pass

class HTM(object):
    def __init__(self, width, length, cellsPerColumn):
        
        #columns is a 2d list of lists, where x and y should line up with indices
        self._column_grid = []
        for x in xrange(width):
            columnsInX = []
            for y in xrange(length):
                columnsInX.append(Column(self, x, y, cellsPerColumn))
            self._column_grid.append(columnsInX)
        
        self.width = width
        self.length = length
        self.inhibitionRadius = config.get('init', 'inhibitionRadius')
        self.cellsPerColumn = cellsPerColumn
        
    @property
    def columns(self):
        for x in xrange(self.width):
            for y in xrange(self.length):
                yield self._column_grid[x][y]
                
    @property
    def columnsActive(self):
        return filter(lambda c: c.active, self.columns)
        
    def initializeInput(self):
        'assume 2d for now'
        #TODO add synapses on input/proximal dendrites from each column to input
        #TODO add synapses on sequential/distal dendrites from each cell to cell
        #TODO more?
        pass 
    
    def neighbors(self, column):
        #boundries
        startx = max(0, column.x - self.inhibitionRadius)
        endx = min(self.width, column.x + self.inhibitionRadius)
        starty = max(0, column.y - self.inhibitionRadius)
        endy = min(self.length, column.y + self.inhibitionRadius)
        
        for x in xrange(startx, endx):
            for y in xrange(starty, endy):
                yield self._column_grid[x][y]

if __name__ == '__main__':
    htm = HTM(
        config.get('init','htm_width'), 
        config.get('init','htm_length'),
        config.get('init','cells_per_column') 
        )
    
    htm.initializeInput()
    
    #TODO enable real data input
    dataTime1 = [[],[],[],[],[]] #2d format, same dimensions as htm (for now)
    dataTime2 = [[],[],[],[],[]]
    data = [dataTime1, dataTime2] 
    
    for inputData in data:
        pool_spatial(htm, inputData)
        pool_temporal(htm, inputData, learning=True)
    
    #TODO show output
    #TODO serialize network state
    pass
