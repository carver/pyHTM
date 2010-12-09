'''
Created on Dec 2, 2010

@author: Jason Carver
'''
from carver.htm.synapse import Synapse

SEGMENT_ACTIVATION_THRESHOLD = 15 #how many synapses need to fire to trigger a segment fire

class Segment(object):
    '''
    A group of synapses that act as a non-linear threshold detector.
    After a certain number of synapses fire, the segment  
    
    Note: a typical threshold for how many synapses on a dendrite need to fire 
    for a spike is 15 (not sure how many synapses total) source 0.1.1 HTM doc,
    Appendix A, distal dendrites, page 55.
    '''


    def __init__(self, distal=True):
        '''
        
        '''
        self.synapses = []
        self.distal = distal
        
    def create_synapse(self, input):
        'input is either the data coming into the layer or the previous cell in network'
        self.add_synapse(Synapse(input))
        
    def add_synapse(self, syn):
        self.synapses.append(syn)
        
    def synapses_firing(self, requireConnection=True):
        '''
        @param requireConnection: only include synapse if the synapse is connected
        @return an iterable of firing synapses
        '''
        return filter(lambda synapse: synapse.is_firing(requireConnection=requireConnection), 
            self.synapses)
    
    def increase_permanences(self, byAmount):
        'increase permanence on all synapses'
        for s in self.synapses:
            s.permanence_increment(byAmount)
            
    @property
    def synapsesConnected(self):
        'return a list of all synapses whose permanence is above the connection threshold'
        return filter(lambda synapse: synapse.connected, self.synapses)
    
    @property
    def active(self):
        '''
        Did the segment fire? ie~ did enough synapses fire to reach the activation threshold
        Timing note: a synapse is considered active if the cell it came from
        was active in the previous step
        '''
        return len(self.synapses_firing()) >= SEGMENT_ACTIVATION_THRESHOLD
    
    @property
    def activeFromLearningCells(self):
        learningSynapses = filter(lambda synapse: synapse.is_firing() and synapse.isInputLearning, 
            self.synapses)
        return len(learningSynapses) >= SEGMENT_ACTIVATION_THRESHOLD
    
    def __str__(self):
        return 'segment active?%s [%s]' % (self.active, ';'.join(map(str,self.synapses)))
