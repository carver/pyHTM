'''
Created on Jan 31, 2011

@author: Jason
'''

class FlashCards(object):
    '''
    This is a state machine that takes a series of 2x2 matrices
    on initialization and a number of steps to display each matrix.
    After the pause (number of steps of dataGenerator calls), 
    FlashCards will update the matrix argument with the next 
    matrix in the series from the initializer.  At the end of
    the list of matrices, FlashCards rotates back to the beginning.
    
    In the context of HTM Networks, this can be used to rotate 
    through a series of static data inputs when training an HTM 
    Network.
    '''    
    
    def __init__(self, pause, *args):
        self.pause = pause
        self.pause_remaining = 0
        self.matrices = args
        self.currentIdx = -1
        
    def dataGenerator(self):
        while True:
            if self.pause_remaining:
                self.pause_remaining -= 1
            else:
                #move to new matrix
                self.currentIdx += 1
                self.currentIdx %= len(self.matrices)
                self.pause_remaining = self.pause - 1
                
            yield self.matrices[self.currentIdx]
                    
    def reset(self):
        self.pause_remaining = 0
        self.currentIdx = -1
        