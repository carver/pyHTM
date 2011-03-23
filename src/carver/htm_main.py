'''
Created on Nov 26, 2010

@author: Jason Carver

'''
from carver.htm import HTM
from carver.htm.ui.excite_history import ExciteHistory
from copy import deepcopy
        
def flipDataGenerator(htm):
    
    #start with non-flipped data
    yield htm._data
    
    while True:
        #flip all data
        dataFlipped = deepcopy(htm._data)
        for x in xrange(len(dataFlipped)):
            for y in xrange(len(dataFlipped[0])):
                dataFlipped[x][y] = not dataFlipped[x][y]
                
        yield dataFlipped

if __name__ == '__main__':
    htm = HTM()
    
    #prepare the initial data image in 2d format, same dimensions as htm, for now
    data = [
        [1,0,1,0,1,0,1,0,1,0],
        [0,0,0,0,1,0,1,0,1,1],
        [0,0,1,0,1,0,0,0,0,1],
        [0,1,0,0,1,1,0,1,0,1],
        [1,0,1,0,1,0,1,0,0,1],
        [0,0,0,1,1,0,0,0,1,1],
        ]
    
    htm.initialize_input(data)
    
    #track htm's data history with
    history = ExciteHistory()
    
    htm.execute(data, flipDataGenerator(htm), ticks=90, postTick=history.update)
    
    #TODO: show output more effectively
    for cell in htm.cells:
        print cell
    for col in htm.columns:
        print col
        
    print "\n\n*************** Graph History **************\n\n"
        
    print history.text_graph()
    
    #TODO: save htm state to disk
