'''
Created on Nov 26, 2010

@author: Jason
'''
from carver.htm.cell import Cell
from carver.htm.synapse import Synapse
from carver.htm.config import config

#using an exponential average, so AS*old+(1-AS*current) => new
AVG_SCALE = 0.995
BOOST_RATE = 1

class Column(object):
    '''
    Represents a column in an HTM network
    '''
    
    MIN_OVERLAP = 5 #TODO choose a reasonable number

    def __init__(self, htm, x, y, cellsPerColumn):
        '''
        
        '''
        self.htm = htm
        self.cells = [Cell() for i in xrange(cellsPerColumn)]
        self.overlap = 0
        #synapses on input/proximal dendrites, forced equal for whole column
        self.synapses = []
        self.boost = 1
        self.x = x
        self.y = y
        self.dutyCycleMin = 0
        self.dutyCycleActive = 0
        self.dutyCycleOverlap = 0
        self.detectingInput = False
        
    def add_synapse(self, x, y):
        'assume 2d input for now; only synapses on column are proximal synapses'
        self.synapses.append(Synapse(x,y))
        
    def synapses_firing(self, inputData):
        return filter(lambda synapse: synapse.is_firing(), self.synapses)
    
    def increase_permanences(self, byAmount):
        for s in self.synapses:
            s.permanence_increment(byAmount)
            
    def input_active(self, active):
        self.detectingInput = active
        
    def get_duty_cycle_active(self):
        newDutyCycle = AVG_SCALE*self.dutyCycleActive
        if self.detectingInput:
            newDutyCycle += (1-AVG_SCALE)
        return newDutyCycle
    
    def get_duty_cycle_overlap(self):
        newDutyCycle = AVG_SCALE*self.dutyCycleOverlap
        if self.overlap > self.MIN_OVERLAP:
            newDutyCycle += (1-AVG_SCALE)
        return newDutyCycle
    
    def next_boost(self):
        if self.dutyCycleActive >= self.dutyCycleMin:
            return 1
        elif self.dutyCycleActive == 0:
            return self.boost * 1.05 #5% growth until you hit something...
        else:
            return self.dutyCycleMin / self.dutyCycleActive
        
    @property
    def synapsesConnected(self):
        return filter(lambda synapse: synapse.connected, self.synapses)
    
    @property
    def neighbors(self):
        return self.htm.neighbors(self)
