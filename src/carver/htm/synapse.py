'''
Created on Nov 27, 2010

@author: Jason Carver
'''
from carver.htm.config import config

CONNECTED_CUTOFF = 0.2 #this is the permanence cutoff to be considered connected
PERMANENCE_INCREMENT = 0.04 #TODO: choose a reasonable number
PERMANENCE_DECREMENT = 0.04 #TODO: choose a reasonable number
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
    
    def was_firing(self, requireConnection=True):
        '''
        Is the input firing?
        @param requireConnection: only return True if the synapse is connected 
            if False: return True even if synapse is not connected
        '''
        return self.input.wasActive and (self.connected or not requireConnection)
    
    def is_firing(self, requireConnection=True):
        '''
        Is the input firing?
        @param requireConnection: only return True if the synapse is connected 
            if False: return True even if synapse is not connected
        '''
        return self.input.active and (self.connected or not requireConnection)
    
    def firing_at(self, timeDelta, requireConnection=True):
        if timeDelta == 0:
            return self.is_firing(requireConnection)
        elif timeDelta == -1:
            return self.was_firing(requireConnection)
        else:
            raise NotImplementedError
    
    def wasInputLearning(self):
        if not hasattr(input, 'learning'):
            return False
        else:
            return input.learning
    
    def permanence_increment(self, increment_by=PERMANENCE_INCREMENT):
        self.permanence = min(self.permanence + increment_by, 1.0)
        
    def permanence_decrement(self, decrement_by=PERMANENCE_DECREMENT):
        self.permanence = max(self.permanence - decrement_by, 0.0)
        
    def __str__(self):
        return '{p:%.3f,c:%s,wf:%s,f:%s}' % (self.permanence, self.connected, self.was_firing(False), self.is_firing(False))

class SynapseState(object):
    
    def __init__(self, synapse, inputWasActive, segment):
        self.synapse = synapse
        self.inputWasActive = inputWasActive
        self.segment = segment
        
    @classmethod
    def captureSegmentState(cls, segment, timeDelta):
        '''
        @param timeDelta: when capturing state, do you capture current or previous state?
            current = 0; previous = -1
        '''
        return map(lambda syn: cls(syn, syn.firing_at(timeDelta, requireConnection=False), segment), segment.synapses)
