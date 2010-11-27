'''
Created on Nov 26, 2010

@author: Jason Carver

Numenta docs are (c) Numenta
'''

def kth_score(columns, k):
    '''
    Numenta docs: Given the list of columns, return the kth highest overlap value
    '''
    pass

def neighbor_duty_cycle_max(column):
    '''
    (Adapted from maxDutyCycle)
    Numenta docs: Returns the maximum active duty cycle of the columns in the 
    given list of colmns  
    '''
    return max([c.duty_cycle for c in column.neighbors])

def average_receptive_field_size(columns):
    '''
    Numenta docs:
    The radius of the average connected receptive field size of all the columns. 
    The connected receptive field size of a column includes only the connected 
    synapses (those with permanence values >= connectedPerm).  This is used 
    to determine the extent of lateral inhibition between columns. 
    '''
    pass

def create_dendrite_segment(htm, cell):
    '''
    set to distal by default
    
    Adapted from getSegmentActiveSynapses() with newSynapses=True
    Numenta docs:
    Return a segmentUpdate data structure containing a list of proposed 
    changes to segment s. Let activeSynapses be the list of active synapses 
    where the originating cells have their activeState output = 1 at time step t.  
    (This list is empty if s = -1 since the segment doesn't exist.) newSynapses 
    is an optional argument that defaults to false. If newSynapses is true, then 
    newSynapseCount - count(activeSynapses) synapses are added to 
    activeSynapses. These synapses are randomly chosen from the set of cells 
    that have learnState output = 1 at time step t. 
    This function iterates through a list of segmentUpdate's and reinforces 
    '''
    pass
