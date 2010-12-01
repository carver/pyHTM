'''
Created on Nov 27, 2010

@author: Jason
'''

class Cell(object):
    '''
    Cell in an HTM network
    
    Note: a typical threshold for how many synapses on a dendrite need to fire 
    for a spike is 15 (not sure how many synapses total) source 0.1.1 HTM doc,
    Appendix A, distal dendrites, page 55.
    '''


    def __init__(self):
        '''
        
        '''
        self.active = False
    
    def active_segments(self, input):
        'prefer distal/sequence over proximal/input, if available'
        pass
