'''
Created on Dec 2, 2010

@author: Jason Carver
'''
from carver.htm.config import config
from carver.htm.synapse import Synapse
import random

#how many synapses need to fire to trigger a segment fire
SEGMENT_ACTIVATION_THRESHOLD = config.getint('constants','synapses_per_segment_threshold')
MAX_NEW_SYNAPSES = config.getint('constants','max_new_synapses')

class Segment(object):
    '''
    A group of synapses that act as a non-linear threshold detector.
    After a certain number of synapses fire, the segment  
    
    Note: a typical threshold for how many synapses on a dendrite need to fire 
    for a spike is 15 (not sure how many synapses total) source 0.1.1 HTM doc,
    Appendix A, distal dendrites, page 55.
    '''


    def __init__(self, distal=True, nextStep=False):
        '''
        @param nextStep: boolean for whether this segment indicates predicted 
            firing in the very next time step 
        '''
        self.synapses = []
        self.distal = distal
        self.nextStep = nextStep
        
    def create_synapse(self, input):
        'input is either the data coming into the layer or the previous cell in network'
        return self.add_synapse(Synapse(input))
        
    def add_synapse(self, syn):
        self.synapses.append(syn)
        return syn
        
    def synapses_firing(self, requireConnection=True):
        '''
        @param requireConnection: only include synapse if the synapse is connected
        @return an iterable of firing synapses
        '''
        return filter(lambda synapse: synapse.is_firing(requireConnection=requireConnection), 
            self.synapses)
        
    def synapses_will_fire(self, requireConnection=True):
        '''
        @param requireConnection: only include synapse if the synapse is connected
        @return an iterable of firing synapses
        '''
        return filter(lambda synapse: synapse.will_fire(requireConnection=requireConnection), 
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
    def activeNext(self):
        '''
        Will the segment fire? Based on current cell active status
        '''
        return len(self.synapses_will_fire()) >= SEGMENT_ACTIVATION_THRESHOLD
    
    @property
    def activeFromLearningCells(self):
        learningSynapses = filter(lambda synapse: synapse.is_firing() and synapse.isInputLearning, 
            self.synapses)
        return len(learningSynapses) >= SEGMENT_ACTIVATION_THRESHOLD
    
    def __str__(self):
        return 'segment active?%s [%s]' % (self.active, ';'.join(map(str,self.synapses)))
    
    @classmethod
    def adapt_up(cls, synapseStates):
        '''HTM v0.1.1 page 46 adaptSegments:
        All active synapses get their permanence counts incremented. All other 
        synapses get their permanence counts decremented. 
        '''
        for state in synapseStates:
            if state.inputWasActive:
                state.synapse.permanence_increment()
            else:
                state.synapse.permanence_decrement()

    @classmethod
    def adapt_down(cls, synapseStates):
        '''HTM v0.1.1 page 46 adaptSegments:
        Synapses on the active list get their permanence counts decremented. 
        '''
        for state in synapseStates:
            if state.inputWasActive:
                state.synapse.permanence_decrement()
                
    def round_out_synapses(self, htm):
        'if not enough synapses active, add more synapses up to configured amount'
        synapses = self.synapses_firing(requireConnection=False)
        
        missingSynapses = MAX_NEW_SYNAPSES - len(synapses)
        if missingSynapses > 0:
            lastLearningCells = filter(lambda cell: cell.wasLearning, htm.cells)
            for _ in xrange(missingSynapses):
                cell = random.choice(lastLearningCells)
                self.create_synapse(cell)
