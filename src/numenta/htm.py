'''
Created on Nov 26, 2010

@author: Numenta, Inc.
translated to python by Jason Carver

Reproduced from "HTM Cortical Learning Algorithms" v0.1.1 at:
http://www.numenta.com/htm-overview/education.php 
'''

from carver.htm.config import config
from carver.htm.synapse import CONNECTED_CUTOFF
from carver.htm.column import Column

#one column out of n should fire:
desiredLocalActivity = config.getint('constants','desiredLocalActivity')

def pool_spatial(htm):
    '''
    A couple notable deviations:
    *column overlap boost and cutoff are swapped from pseudocode, details inline
        see _spatial_overlap
    *time and inputData removed from code - used a data producer model, linked to htm 
    '''
    
    _spatial_overlap(htm)
    
    activeColumns = _spatial_inhibition(htm)
            
    inhibitionRadius = _spatial_learning(htm, activeColumns)
    
    htm.inhibitionRadius = inhibitionRadius

def pool_temporal(htm, learning=True):
    updateSegments = _temporal_phase1(htm, learning)
            
    updateSegments = _temporal_phase2(htm, updateSegments, learning)
    
    if learning:
        _temporal_phase3(htm, updateSegments)
    
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

def _temporal_phase1(htm, learning):
    'Phase 1, p40'
    
    #hash from cell to a list of segments
    updateSegments = {}
    
    for col in htm.columns_active():
        buPredicted = False
        learningCellChosen = False
        for i in xrange(htm.cellsPerColumn):
            cell = col.cells[i]
            if cell.predicted:
                seg = cell.activeSegment() #TODO always return segment or protect against None
                
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
            cell = col.bestCell()
            cell.learning = True
            seg = cell.create_segment(htm)
            updateSegments[cell] = [seg]
            
    return updateSegments
            
def _temporal_phase2(htm, updateSegments, learning):
    'Phase 2, p40'
    for cell in htm.cells:
        if learning and cell not in updateSegments:
            updateSegments[cell] = []
            
        for seg in cell.segments:
            if seg.active:
                cell.predicting = True
                
                if learning:
                    updateSegments[cell].append(seg)
            
        #for each cell, grab the best segment. right now, this does not prevent 
        #duplication of learning on the best segment
        if learning and cell.predicting:
            bestSeg = cell.bestMatchingSegment()
            updateSegments[cell].append(bestSeg)
    
    return updateSegments

def _temporal_phase3(htm, updateSegments):
    'Phase 3, p42'
    for cell in htm.cells:
        if cell.learning:
            for seg in updateSegments[cell]:
                seg.adapt_up()
        elif not cell.predicting and cell.predicted:
            for seg in updateSegments[cell]:
                seg.adapt_down()
