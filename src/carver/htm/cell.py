'''
Created on Nov 27, 2010

@author: Jason
'''
from carver.htm.config import config
from carver.htm.segment import Segment
from carver.htm.synapse import MIN_THRESHOLD, SYNAPSES_PER_SEGMENT
from random import random

SEGMENTS_PER_CELL = config.get('init','segments_per_cell')

class Cell(object):
    '''
    Cell in an HTM network
    '''


    def __init__(self):
        '''
        
        '''
        self.active = False
        self.__wasActive = False #read-only
        self.predicting = False
        self.__predicted = False #read-only
        self.learning = False
        self.__wasLearning = False #read-only
        
        self.segments = [Segment() for i in xrange(SEGMENTS_PER_CELL)]
       
    @property
    def wasActive(self):
        return self.__wasActive
    
    @property
    def wasLearning(self):
        return self.__wasLearning
    
    @property
    def predicted(self):
        return self.__predicted
    
    def clockTick(self):
        self.__predicted = self.predicting
        self.__wasActive = self.active
        self.__wasLearning = self.learning
        
        self.predicting = False
        self.active = False
        self.learning = False
    
    def active_segments(self, input):
        'prefer distal/sequence over proximal/input, if available'
        pass
    
    def create_segment(self, htm):
        seg = Segment()
        
        #randomly choose input cells
        wasLearningCells = filter(lambda c: c.wasLearning, htm.cells)
        inputCells = random.sample(wasLearningCells, SYNAPSES_PER_SEGMENT)
        
        for i in xrange(SYNAPSES_PER_SEGMENT):
            seg.add_synapse(inputCells[i])
            
        self.segments.append(seg)
        
        return seg
    
    def __hash__(self):
        return 1 #TODO make hashable
    
    @property
    def activeSegment(self):
        'prefer distal'
        for seg in self.segments:
            if seg.active:
                return seg
            
    @property
    def bestMatchingSegment(self):
        '''
        For this cell, find the segment with the largest 
        number of active synapses. This routine is aggressive in finding the best 
        match. The permanence value of synapses is allowed to be below 
        connectedPerm. The number of active synapses is allowed to be below 
        activationThreshold, but must be above minThreshold. The routine 
        returns the segment index. If no segments are found, then None is 
        returned. 
        '''
        bestSegment = None
        bestSegmentSynapseCount = MIN_THRESHOLD
        for seg in self.segments:
            synapseCount = len(seg.synapses_firing(acrossSynapse=False))
            if synapseCount > bestSegmentSynapseCount:
                bestSegmentSynapseCount = synapseCount
                bestSegment = seg
                
        return bestSegment
