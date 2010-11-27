'''
Created on Nov 26, 2010

@author: Numenta, Inc.
translated to python by Jason Carver

Reproduced from "HTM Cortical Learning Algorithms" v0.1.1 at:
http://www.numenta.com/htm-overview/education.php 
'''

from carver.htm import kth_score, neighbor_duty_cycle_max, average_receptive_field_size,\
    create_dendrite_segment

MIN_OVERLAP = 5 #TODO choose a reasonable number
PERMANENCE_INCREMENT = 0.04 #TODO choose a reasonable number
PERMANENCE_DECREMENT = 0.04 #TODO choose a reasonable number

#one column out of n should fire:
desiredLocalActivity = 50 # TODO choose a reasonable number

def pool_spatial(htm, input):
    '''
    A couple notable deviations:
    *column overlap boost and cutoff are swapped from pseudocode, details inline
    *time (t) removed from code - assuming that data is already sliced by time 
    '''
    
    columns = htm.columns
    
    #Overlap, p 35
    _spatial_overlap(columns)
    
    #Inhibition, p 35
    activeColumns = _spatial_inhibition(columns)
            
    #Learning, p 36
    inhibitionRadius = _spatial_learning(columns, activeColumns)
    
    return inhibitionRadius

def pool_temporal(htm, input, learning=True):
    #These phases can be written more pythonically, but it would lose the pseudocode feel
    
    #Phase 1, p40
    _temporal_phase1(htm, learning)
            
    #Phase 2, p40
    updateSegments = _temporal_phase2(htm, learning)
    
    #Phase 3, p42
    if learning:
        _temporal_phase3(htm, updateSegments)
    
def _spatial_overlap(columns):
    for c in columns:
        c.overlap = 0
        for s in c.synapsesConnected:
            c.overlap += s.is_firing(input)
            
        #The paper has conflicting information in the following lines.
        #The text implies boost before cutoff, the code: cutoff then boost. I 
        #chose boost first because I think the boost should help a column 
        #overcome the cutoff. This is based solely on intuitin. 
        c.overlap *= c.boost
        
        if c.overlap < MIN_OVERLAP:
            c.overlap = 0
    
def _spatial_inhibition(columns):
    activeColumns = []
    for c in columns:
        minLocalActivity = kth_score(c.neighbors, desiredLocalActivity)
        
        if c.overlap > 0 and c.overlap >= minLocalActivity:
            activeColumns.append(c)
    
    return activeColumns

def _spatial_learning(columns, activeColumns):
    for c in activeColumns:
        for s in c.synapses:
            if s.is_firing(input):
                s.permanence += PERMANENCE_INCREMENT
                s.permanence = min(s.permanence, 1.0)
            else:
                s.permanence += PERMANENCE_DECREMENT
                s.permanence = max(s.permanence, 0.0)
            
    for c in columns:
        c.min_duty_cycle = 0.01 * neighbor_duty_cycle_max(c)
        c.duty_cycle = c.next_duty_cycle()
        c.boost = c.next_boost()
        
    return average_receptive_field_size(columns)

def _temporal_phase1(htm, learning):
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
            
def _temporal_phase2(htm, input, learning):
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
            bestSeg = cell.best_potential_segment(input)
            updateSegments[cell].append(bestSeg)
    
    return updateSegments

def _temporal_phase3(htm, updateSegments):
    for cell in htm.allCells:
        if cell.learning:
            for seg in updateSegments[cell]:
                seg.adapt_up()
        elif not cell.predicting and cell.predicted:
            for seg in updateSegments[cell]:
                seg.adapt_down()

if __name__ == '__main__':
    pass