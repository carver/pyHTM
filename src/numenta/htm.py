'''
Created on Nov 26, 2010

@author: Numenta, Inc.
translated to python by Jason Carver

Reproduced from "HTM Cortical Learning Algorithms" v0.1.1 at:
http://www.numenta.com/htm-overview/education.php 
'''

from carver.htm import kth_score, neighbor_duty_cycle_max, average_receptive_field_size,\
    create_dendrite_segment
from carver.htm.config import config
from carver.htm.synapse import CONNECTED_CUTOFF

#one column out of n should fire:
desiredLocalActivity = config.get('constants','desiredLocalActivity')

def pool_spatial(htm, inputData):
    '''
    A couple notable deviations:
    *column overlap boost and cutoff are swapped from pseudocode, details inline
    *time (t) removed from code - assuming that data is already sliced by time 
    '''
    
    _spatial_overlap(htm)
    
    activeColumns = _spatial_inhibition(htm)
            
    inhibitionRadius = _spatial_learning(htm, activeColumns, inputData)
    
    htm.inhibitionRadius = inhibitionRadius

def pool_temporal(htm, inputData, learning=True):
    _temporal_phase1(htm, learning)
            
    updateSegments = _temporal_phase2(htm, learning)
    
    if learning:
        _temporal_phase3(htm, updateSegments)
    
def _spatial_overlap(htm, inputData):
    'Overlap, p 35'
    
    for c in htm.columns:
        c.overlap = len(c.synapses_firing(inputData))
            
        #The paper has conflicting information in the following lines.
        #The text implies boost before cutoff, the code: cutoff then boost. I 
        #chose boost first because I think the boost should help a column 
        #overcome the cutoff. This choice is based solely on intuition. 
        c.overlap *= c.boost
        
        if c.overlap < c.MIN_OVERLAP:
            c.overlap = 0
    
def _spatial_inhibition(htm):
    'Inhibition, p 35'
    activeColumns = []
    for c in htm.columns:
        minLocalActivity = kth_score(htm.neighbors(c), desiredLocalActivity)
        
        if c.overlap > 0 and c.overlap >= minLocalActivity:
            activeColumns.append(c)
            c.input_active(True)
        else:
            c.input_active(False)
    
    return activeColumns

def _spatial_learning(htm, activeColumns, inputData):
    'Learning, p 36'
    for c in activeColumns:
        for s in c.synapses:
            if s.is_firing(inputData):
                s.permanence_increment()
            else:
                s.permanence_decrement()
            
    for c in htm.columns:
        c.dutyCycleMin = 0.01 * neighbor_duty_cycle_max(c)
        c.dutyCycleActive = c.get_duty_cycle_active()
        c.boost = c.next_boost()
        
        c.dutyCycleOverlap = c.get_duty_cycle_overlap()
        if c.dutyCycleOverlap < c.dutyCycleMin:
            c.increase_permanences(0.1 * CONNECTED_CUTOFF)
        
    return average_receptive_field_size(htm.columns) #TODO

def _temporal_phase1(htm, learning):
    'Phase 1, p40'
    for c in htm.columnsActive:
        buPredicted = False
        lcChosen = False
        for i in xrange(htm.cellsPerColumn):
            cell = c.cells[i]
            if cell.predicted:
                seg = cell.mostActiveSegment
                
                #distal dendrite segments = sequence memory
                if seg.wasActive and seg.distal:
                    buPredicted = True
                    cell.active = True
                    
                    #Learning Phase 1, p 41
                    if learning and cell.learning:
                        lcChosen = True
                        cell.learning = True
                    
                    
        if not buPredicted:
            for cell in c.cells:
                cell.active = True
                
        #Learning Phase 1, p41
        if learning and not lcChosen:
            cell = c.bestCell
            cell.learning = True
            seg = create_dendrite_segment(htm, cell)
            cell.segments.append(seg)
            
def _temporal_phase2(htm, inputData, learning):
    'Phase 2, p40'
    
    #hash from cell to a list of segments
    updateSegments = {}
    
    for cell in htm.allCells:
        updateSegments[cell] = []
        for seg in cell.segments:
            if seg.active:
                cell.predicting = True
                
                if learning:
                    updateSegments[cell].append(seg)
            
        #for each cell, grab the best segment. right now, this does not prevent 
        #duplication of learning on the best segment
        if learning and cell.predicting:
            bestSeg = cell.best_potential_segment(inputData)
            updateSegments[cell].append(bestSeg)
    
    return updateSegments

def _temporal_phase3(htm, updateSegments):
    'Phase 3, p42'
    for cell in htm.allCells:
        if cell.learning:
            for seg in updateSegments[cell]:
                seg.adapt_up()
        elif not cell.predicting and cell.predicted:
            for seg in updateSegments[cell]:
                seg.adapt_down()
