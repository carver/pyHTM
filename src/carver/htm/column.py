'''
Created on Nov 26, 2010

@author: Jason
'''
from carver.htm.cell import Cell
from carver.htm.synapse import Synapse

class Column(object):
    '''
    Represents a column in an HTM network
    '''
    
    MIN_OVERLAP = 5 #TODO choose a reasonable number

    def __init__(self, x, y, cellsPerColumn):
        '''
        
        '''
        self.cells = [Cell() for i in xrange(cellsPerColumn)]
        self.overlap = None
        #synapses on input/proximal dendrites, forced equal for whole column
        self.synapses = []
        self.boost = 1
        self.x = x
        self.y = y
        
    def add_synapse(self, x, y):
        'assume 2d input for now; only synapses on column are proximal synapses'
        self.synapses.append(Synapse(x,y))
        
    def synapses_firing(self, inputData):
        return filter(lambda synapse: synapse.is_firing(), self.synapses)
        
    @property
    def synapsesConnected(self):
        return filter(lambda synapse: synapse.connected, self.synapses)
