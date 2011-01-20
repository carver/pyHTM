'''
Created on Jan 19, 2011

@author: Jason
'''

class ExciteHistory(object):
    '''
    Track the history of an HTM, in order to graph a summary.
    '''


    def __init__(self):
        '''
        '''
        self.data = []
        self.numCells = 0
        
    def update(self, htm):
        timeSlice = []
        for cell in htm.cells:
            state = 0
            if cell.active:
                state = 2
            elif cell.predicting:
                state = 1
            timeSlice.append(state)
            
        self.numCells = max(self.numCells, len(timeSlice))
            
        self.data.append(timeSlice)
        
    def _state_to_char(self, state):
        if state == 0: return ' '
        elif state == 1: return '.'
        elif state == 2: return '0'
        else: return '?'
        
    def text_graph(self):
        #TODO handle variable cells well 
        rows = []
        for i in xrange(self.numCells):
            rows.append([])
            
        for slice in self.data:
            for i, state in enumerate(slice):
                rows[i].append(self._state_to_char(state))
            
        lines = map(lambda row: ''.join(row), rows)
        
        return '\n'.join(lines)
