'''
Created on Mar 28, 2011

@author: Jason
'''

class DictDefault(dict):
    '''
    a dictionary that starts fresh with a value by calling a supplied function
    '''


    def __init__(self, newValueFunc=list, *args, **kwargs):
        '''
        Constructor
        '''
        dict.__init__(*args, **kwargs)
        self.newValueFunc = newValueFunc
        
    def __getitem__(self, key):
        if not dict.has_key(key):
            dict.__setitem__(self,key,self.newValueFunc())
        return dict.__getitem__(self, key)
