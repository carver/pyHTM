'''
Created on Nov 27, 2010

@author: Jason
'''
from carver.htm.config import config
from carver.htm.segment import Segment
from carver.htm.synapse import MIN_THRESHOLD, SYNAPSES_PER_SEGMENT
import random

SEGMENTS_PER_CELL = config.getint('init','segments_per_cell')

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
    
    def create_segment(self, htm, nextStep):
        '''
        @param htm: the htm network that contains the cell
        @param nextStep: boolean for whether this segment indicates predicted 
            firing in the very next time step 
        '''
        seg = Segment(nextStep=nextStep)
        
        #randomly choose input cells, from 
        synapseLen = self.__createSynapses(seg, htm.cells, SYNAPSES_PER_SEGMENT,
            lambda c: c.wasLearning)
        
        if synapseLen < SYNAPSES_PER_SEGMENT:
            addSynapseLen = SYNAPSES_PER_SEGMENT - synapseLen
            activeSynapseLen = self.__createSynapses(seg, htm.cells, addSynapseLen,
                lambda c: c.wasActive)
        
            if activeSynapseLen < SYNAPSES_PER_SEGMENT:
                addSynapseLen -= activeSynapseLen
                self.__createSynapses(seg, htm.cells, addSynapseLen, None)
            
        self.segments.append(seg)
        
        return seg
    
    def __createSynapses(self, segment, cells, maxSynapses, filterFunc):
        matchingCells = filter(filterFunc, cells)
        sampleSize = min(len(matchingCells), maxSynapses)
        synapseFrom = random.sample(matchingCells, sampleSize)
        
        for cell in synapseFrom:
            segment.create_synapse(cell)
             
        return len(synapseFrom)
    
    def __hash__(self):
        return 1 #TODO: make hashable
    
    def activeSegment(self):
        'prefer distal'
        for seg in self.segments:
            if seg.active:
                return seg
            
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
            synapseCount = len(seg.synapses_firing(requireConnection=False))
            if synapseCount > bestSegmentSynapseCount:
                bestSegmentSynapseCount = synapseCount
                bestSegment = seg
                
        return bestSegment
    
    def __str__(self):
        #TODO: show synapses
        base = "cell: (active,predicting,learning) = now(%s,%s,%s) last(%s,%s,%s)" % (
            self.active, self.predicting, self.learning, self.wasActive, 
            self.predicted, self.wasLearning)
        
        segText = [base]
        for seg in self.segments:
            segText.append(str(seg))
            
        return '\n\t'.join(segText)
