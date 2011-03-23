'''
Created on Jan 31, 2011

@author: Jason
'''

class TranslateInput(object):
    '''
    Take an input matrix and shift it over time.
    '''    
    
    def __init__(self, init, shift, steps=None):
        '''
        @param init: a data matrix to start with
        @param shift: a list with one element for each dimension of the init matrix,
            representing the shift per time step
        @param steps: Number of steps to execute
        '''
        self.current = init
        self.steps_remaining = steps if steps is not None else -1
        self.shift = shift
        
    def dataGenerator(self):
        
        #start by returning the first data matrix
        yield  self.current
        
        while self.steps_remaining:
            
            self.current = self.doShift()
            
            yield self.current
            
            self.steps_remaining -= 1
            
    def doShift(self):
        
        #shift X
        shifted = self.__shiftList(self.current, self.shift[0])
        
        #shift Y
        if len(self.shift) > 1:
            shifted = [ self.__shiftList(dim, self.shift[1]) for dim in shifted ]
        
        return shifted
    
    def __shiftList(self, original, byX):
        if byX:
            #shift along the X axis
            shifted = original[byX*-1:]
            shifted.extend(original[:byX*-1])
            
            return shifted
        else:
            return original
