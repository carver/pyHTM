'''
Created on Nov 26, 2010

@author: Jason Carver

'''
from carver.htm import HTM
from carver.htm.ui.excite_history import ExciteHistory

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
    
    #this method should update the data matrix in place
    def dataUpdate(data):
        'flip all bits in data matrix'
        for x in xrange(len(data)):
            data[x]=map(lambda bit: not bit, data[x])
    
    #track htm's data history with
    history = ExciteHistory()
    
    htm.execute(data, dataUpdate, ticks=90, postTick=history.update)
    
    #TODO show output more effectively
    for cell in htm.cells:
        print cell
    for col in htm.columns:
        print col
        
    print "\n\n*************** Graph History **************\n\n"
        
    print history.text_graph()
    
    #TODO save htm state to disk
