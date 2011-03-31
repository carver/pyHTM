'''
Created on Dec 3, 2010

@author: Jason Carver
'''

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
        #TODO move magic number 0.8 into .properties file, or make htm understand float
        self.stimulationPast = 1 if self.stimulation > 0.8 else 0
        self.resetStimulation()
        
        
