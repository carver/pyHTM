'''
Created on Nov 27, 2010

@author: Jason Carver
'''

CONNECTED_CUTOFF = 0.2 #this is the permanence cutoff to be considered connected
PERMANENCE_INCREMENT = 0.04 #TODO choose a reasonable number
PERMANENCE_DECREMENT = 0.04 #TODO choose a reasonable number

class Synapse(object):
    '''
    a single synapse between dendrite and axon
    '''


    def __init__(self, x, y, permanence = (CONNECTED_CUTOFF-.001)):
        '''
        '''
        self.x = x
        self.y = y
        self.permanence = permanence
        
    @property
    def connected(self):
        return self.permanence >= CONNECTED_CUTOFF
    
    def is_firing(self, inputData):
        return inputData[self.x][self.y]
    
    def permanence_increment(self, increment_by=PERMANENCE_INCREMENT):
        self.permanence = min(self.permanence + increment_by, 1.0)
        
    def permanence_decrement(self, decrement_by=PERMANENCE_DECREMENT):
        self.permanence = max(self.permanence - decrement_by, 0.0)
