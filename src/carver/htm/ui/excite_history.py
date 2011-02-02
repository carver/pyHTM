'''
Created on Jan 19, 2011

@author: Jason
'''

class ExciteHistory(object):
    '''
    Track the history of an HTM, in order to graph a summary.
    '''
    INACTIVE = 0
    PREDICTING = 1
    ACTIVE = 2

    def __init__(self, temporal=True):
        '''
        '''
        self.data = []
        self.dataLen = 0
        self.temporal = temporal
        
    def update(self, htm):
        timeSlice = []
        
        if self.temporal:
            for cell in htm.cells:
                state = self.INACTIVE
                if cell.active:
                    state = self.ACTIVE
                elif cell.predicting:
                    state = self.PREDICTING
                timeSlice.append(state)
        else:
            for col in htm.columns:
                state = self.INACTIVE
                if col.active:
                    state = self.ACTIVE
                timeSlice.append(state)
            
        self.dataLen = max(self.dataLen, len(timeSlice))
            
        self.data.append(timeSlice)
        
    def _state_to_char(self, state):
        if state == self.INACTIVE: return ' '
        elif state == self.PREDICTING: return '.'
        elif state == self.ACTIVE: return '0'
        else: return '?'
        
    def text_graph(self):
        #TODO handle variable cells well 
        rows = []
        for i in xrange(self.dataLen):
            rows.append([])
            
        for slice in self.data:
            for i, state in enumerate(slice):
                rows[i].append(self._state_to_char(state))
            
        lines = map(lambda row: ''.join(row), rows)
        
        return '\n'.join(lines)
