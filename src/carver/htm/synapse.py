'''
Created on Nov 27, 2010

@author: Jason Carver
'''
from carver.htm.config import config

CONNECTED_CUTOFF = 0.2 #this is the permanence cutoff to be considered connected
PERMANENCE_INCREMENT = 0.04 #TODO choose a reasonable number
PERMANENCE_DECREMENT = 0.04 #TODO choose a reasonable number
MIN_THRESHOLD = config.getint('constants','min_synapses_per_segment_threshold')
SYNAPSES_PER_SEGMENT = config.getint('init', 'synapses_per_segment')

class Synapse(object):
    '''
    a single synapse between dendrite and axon
    '''


    def __init__(self, input, permanence = (CONNECTED_CUTOFF-.001)):
        '''
        @param input: the source of data coming into the synapse
        synapses on distal dendrites will have a Cell as input
        synapses on proximal dendrites will have an InputCell as input
        '''
        self.permanence = permanence
        self.input = input
        
    @property
    def connected(self):
        return self.permanence >= CONNECTED_CUTOFF
    
    def is_firing(self, acrossSynapse=True):
        '''
        Is the input firing?
        @param acrossSynapse: only return True if the synapse is connected 
        '''
        return self.input.wasActive and (self.connected or not acrossSynapse)
    
    def isInputLearning(self):
        if not hasattr(input, 'learning'):
            return False
        else:
            return input.learning
    
    def permanence_increment(self, increment_by=PERMANENCE_INCREMENT):
        self.permanence = min(self.permanence + increment_by, 1.0)
        
    def permanence_decrement(self, decrement_by=PERMANENCE_DECREMENT):
        self.permanence = max(self.permanence - decrement_by, 0.0)
