'''
Created on Nov 26, 2010

@author: Numenta, Inc.
translated to python by Jason Carver

Reproduced from "HTM Cortical Learning Algorithms" v0.1.1 at:
http://www.numenta.com/htm-overview/education.php 
'''

from carver.htm.config import config
from carver.htm.synapse import CONNECTED_CUTOFF
from carver.utilities.dict_default import DictDefault

#one column out of n should fire:
desiredLocalActivity = config.getint('constants','desiredLocalActivity')

def pool_spatial(htm):
    '''
    A couple notable deviations:
    *column overlap boost and cutoff are swapped from pseudocode, details inline
        see _spatial_overlap
    *time and inputData removed from code - used a data producer model, linked to htm 
    *getBestMatchingSegment now takes an argument for whether it is a nextStep segment or a sequence one
        inspired by binarybarry on http://www.numenta.com/phpBB2/viewtopic.php?t=1403
    '''
    
    _spatial_overlap(htm)
    
    activeColumns = _spatial_inhibition(htm)
            
    inhibitionRadius = _spatial_learning(htm, activeColumns)
    
    htm.inhibitionRadius = inhibitionRadius

def pool_temporal(htm, updateSegments, learning=True):
    updateSegments = _temporal_phase1(htm, learning, updateSegments)
            
    updateSegments = _temporal_phase2(htm, updateSegments, learning)
    
    if learning:
        updateSegments = _temporal_phase3(htm, updateSegments)
    
    return updateSegments
    
def _spatial_overlap(htm):
    'Overlap, p 35'
    
    for col in htm.columns:
        col.overlap = len(col.synapses_firing())
            
        #The paper has conflicting information in the following lines.
        #The text implies boost before cutoff, the code: cutoff then boost. I 
        #chose boost first because I think the boost should help a column 
        #overcome the cutoff.
        col.overlap *= col.boost
        
        if col.overlap < col.MIN_OVERLAP:
            col.overlap = 0
    
def _spatial_inhibition(htm):
    'Inhibition, p 35'
    activeColumns = []
    for col in htm.columns:
        kthNeighbor = col.kth_neighbor(desiredLocalActivity)
        minLocalActivity = kthNeighbor.overlap
        
        if col.overlap > 0 and col.overlap >= minLocalActivity:
            activeColumns.append(col)
            col.active = True
        else:
            col.active = False
    
    return activeColumns

def _spatial_learning(htm, activeColumns):
    'Learning, p 36'
    for col in activeColumns:
        for s in col.synapses:
            if s.is_firing():
                s.permanence_increment()
            else:
                s.permanence_decrement()
            
    for col in htm.columns:
        col.dutyCycleMin = 0.01 * col.neighbor_duty_cycle_max()
        col.dutyCycleActive = col.get_duty_cycle_active()
        col.boost = col.next_boost()
        
        col.dutyCycleOverlap = col.get_duty_cycle_overlap()
        if col.dutyCycleOverlap < col.dutyCycleMin:
            col.increase_permanences(0.1 * CONNECTED_CUTOFF)
        
    return htm.average_receptive_field_size()

def _temporal_phase1(htm, learning, updateSegments):
    '''
    Phase 1, p40
    @param htm: htm network object
    @param learning: boolean describing whether the network is learning now
    @param updateSegments: hash from cell to a list of segments to update when cell becomes active
    '''
    
    for col in htm.columns_active():
        buPredicted = False
        learningCellChosen = False
        for cell in col.cells:
            if cell.predicted:
                seg = cell.activeSegment() #TODO: always return segment or protect against None
                
                #distal dendrite segments = sequence memory
                if seg and seg.distal:
                    buPredicted = True
                    cell.active = True
                    
                    #Learning Phase 1, p 41
                    if learning and seg.activeFromLearningCells:
                        learningCellChosen = True
                        cell.learning = True
                    
        if not buPredicted:
            for cell in col.cells:
                cell.active = True
                
        #Learning Phase 1, p41
        if learning and not learningCellChosen:
            cell, seg = col.bestCell(nextStep=True)
            cell.learning = True
            
            if seg is None:
                seg = cell.create_segment(htm, nextStep=True)
                
            updateSegments[cell].append(seg)
            
    return updateSegments
            
def _temporal_phase2(htm, updateSegments, learning):
    'Phase 2, p40'
    for cell in htm.cells:
        for seg in cell.segments:
            if seg.active:
                cell.predicting = True
                
                if learning:
                    updateSegments[cell].append(seg)
            
        #for each cell, grab the best segment. right now, this does not prevent 
        #duplication of learning on the best segment
        if learning and cell.predicting:
            bestSeg = cell.bestMatchingSegment(nextStep=False)
            if bestSeg is None:
                bestSeg = cell.create_segment(htm, nextStep=False)
            updateSegments[cell].append(bestSeg)
    
    return updateSegments

def _temporal_phase3(htm, updateSegments):
    'Phase 3, p42'
    for cell in htm.cells:
        if cell.learning:
            for seg in updateSegments[cell]:
                seg.adapt_up()
            updateSegments[cell] = []
        elif not cell.predicting and cell.predicted:
            for seg in updateSegments[cell]:
                seg.adapt_down()
            updateSegments[cell] = []
            
    return updateSegments
