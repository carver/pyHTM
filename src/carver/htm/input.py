'''
Created on Dec 3, 2010

@author: Jason Carver
'''

class InputCell(object):
    '''
    a single pixel of input
    '''


    def __init__(self, x, y, inputData):
        '''
        @param x: x location of input data
        @param y: y location of input data
        @param inputData: a mutable binary 2-d array of data that represents incoming senses 
        '''
        self.x = x
        self.y = y
        self.inputData = inputData
        self.predicted = False
        
    @property
    def wasActive(self):
        return self.inputData[self.x][self.y]
    
    @property
    def location(self):
        return [self.x, self.y]
