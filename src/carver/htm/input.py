'''
Created on Dec 3, 2010

@author: Jason Carver
'''
from carver.htm.synapse import SYNAPSES_PER_SEGMENT
from carver.htm.segment import FRACTION_SEGMENT_ACTIVATION_THRESHOLD

class InputCell(object):
    '''
    a single pixel of input
    '''


    def __init__(self, x, y, inputData):
        '''
        @param x: x location of input data
        @param y: y location of input data
        @param inputData: a mutable binary 2-d array of data that represents incoming senses 
        '''
        self.x = x
        self.y = y
        self.inputData = inputData
        self.predicted = False
        
        #currently used for downstream stimulation ("imagination")
        self.resetStimulation()
        self.overrideInput = False
        self.stimulationPast = 0
        
        #this should not be called in normal circumstances and is preventing 
        #    an attribute exception when synapse calls it for display purposes
        self.active = False
        
    def resetStimulation(self):
        self.stimulation = 0.0
        
    @property
    def wasActive(self):
        if self.overrideInput:
            return self.stimulationPast
        else:
            return self.inputData[self.x][self.y]
    
    @property
    def location(self):
        return [self.x, self.y]
    
    def stimulate(self, amount):
        self.stimulation += amount
        
    def override(self):
        self.overrideInput = True
        
        if self.stimulation >= FRACTION_SEGMENT_ACTIVATION_THRESHOLD:
            self.stimulationPast = 1
        else:
            self.stimulationPast = 0
            
        self.resetStimulation()
        
        
