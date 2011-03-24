'''
Created on Nov 26, 2010

@author: Jason Carver

'''
from carver.htm import HTM
from carver.htm.ui.excite_history import ExciteHistory
from copy import deepcopy
from carver.htm.io.image_builder import ImageBuilder
        
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
    
    htm.execute(flipDataGenerator(htm), ticks=180, postTick=history.update)
        
    print """*************** Graph History **************
Y-Axis: All cells in the network, with the 4 cells per column grouped together
X-Axis: Time
Colors:
\tblack: no activity
\tgray: predicting
\twhite: active
    
Notice that the network settles down very quickly at the left, but not completely.  You will typically see artifacts around 100 steps in (about halfway across the image).

At each time step, the input data is flipping bits. So you will see some cells alternating at every time step, some cells that are active either way, and some cells that are never active.  
"""
    
    ## Show image with history grouped by cell
    columnStates = history.data
    
    def stateToRGB(state):
        if state == ExciteHistory.ACTIVE:
            return (255, 255, 255)
        elif state == ExciteHistory.PREDICTING:
            return (127, 127, 127)
        elif state == ExciteHistory.INACTIVE:
            return (0, 0, 0)
        else:
            return (255, 0, 0) #unknown cell/column state
    
    img = ImageBuilder([len(columnStates[0]), len(columnStates)], stateToRGB)
    img.setData2D(columnStates)
    img.rotate90()
    img.show()
