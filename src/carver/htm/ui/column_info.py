'''
Created on Feb 7, 2011

@author: Jason
'''

class ColumnInfo(object):
    '''
    classdocs
    '''


    def __init__(self, column):
        '''
        Constructor
        '''
        self.col = column
        
    def legend(self):
        return '''Incoming Spike: 'O' (Connected); 'X' (Unconnected)\nNo Activity: '_' (Connection); '.' (Unconnected) '''
        
    def synapseStates(self):
        states = []
        for syn in self.col.synapses:
            state = '?'
            inputFiring = syn.is_firing(requireConnection=False)
            if syn.connected:
                if inputFiring:
                    state = 'O'
                else:
                    state = '_'
            else:
                if inputFiring:
                    state = 'X'
                else:
                    state = '.'
            states.append(state)
        return ' '.join(states)
        
    def synapseTargets(self):
        return ' '.join(map(lambda syn: str(syn.input.location), self.col.synapses))
