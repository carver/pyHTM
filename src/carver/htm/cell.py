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


    def __init__(self, column, layer):
        '''
        @param layer the inner layer of the cell, so an HTM with 3 cells per column
            would have cells with layers 0, 1 and 2
        '''
        self.column = column
        self.layer = layer
        
        self.active = False
        self.__wasActive = False #read-only
        self.predicting = False
        self.__predicted = False #read-only
        self.learning = False
        self.__wasLearning = False #read-only
        self.predictingNext = None #cached-val
        self.__predictedNext = False #read-only
        
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
    
    @property
    def predictedNext(self):
        return self.__predictedNext
    
    @property
    def segmentsNear(self):
        return self.__segmentsFilterNextStep(True)
    
    @property
    def segmentsFar(self):
        return self.__segmentsFilterNextStep(False)
    
    @property
    def predictingNext(self):
        if self.__predictingNext is not None:
            return self.__predictingNext
        
        cache = False
        for segment in self.segmentsNear:
            if segment.active:
                cache = True
                break
            
        self.__predictingNext = cache
        return self.__predictingNext
    
    @predictingNext.setter
    def predictingNext(self, value):
        self.__predictingNext = value
    
    def __segmentsFilterNextStep(self, nextStep):
        return filter(lambda seg: seg.nextStep == nextStep, self.segments)
    
    def clockTick(self):
        self.__predicted = self.predicting
        self.__wasActive = self.active
        self.__wasLearning = self.learning
        self.__predictedNext = self.predictingNext
        
        self.predicting = False
        self.predictingNext = None
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
        
        #randomly choose input cells, from active non-self cells
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
        alsoFilterSelf = lambda cell: filterFunc(cell) and cell!=self
        
        matchingCells = filter(alsoFilterSelf, cells)
        sampleSize = min(len(matchingCells), maxSynapses)
        synapseFrom = random.sample(matchingCells, sampleSize)
        
        for cell in synapseFrom:
            segment.create_synapse(cell)
             
        return len(synapseFrom)
    
    def __hash__(self):
        return self.layer * hash(self.column)
    
    def __eq__(self, other):
        if not hasattr(other, 'column') or not hasattr(other, 'layer'):
            return False
        return self.layer == other.layer and self.column == other.column
    
    def activeSegmentNear(self):
        'prefer distal, return hits from segments connected to other cells that were active'
        for seg in self.segmentsNear:
            if seg.active:
                return seg
            
    def bestMatchingSegment(self, nextStep):
        '''
        For this cell, find the segment with the largest 
        number of active synapses. This routine is aggressive in finding the best 
        match. The permanence value of synapses is allowed to be below 
        connectedPerm. The number of active synapses is allowed to be below 
        activationThreshold, but must be above minThreshold. The routine 
        returns the segment index. If no segments are found, then None is 
        returned. 
        @param nextStep: should the segment be of the nextStep type, or all-time prediction?
        '''
        bestSegment = None
        bestSegmentSynapseCount = MIN_THRESHOLD
        for seg in filter(lambda seg: seg.nextStep == nextStep, self.segments):
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
