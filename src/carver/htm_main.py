'''
Created on Nov 26, 2010

@author: Jason Carver

Numenta docs are (c) Numenta
'''
from carver.htm.config import config
from carver.htm import HTM
from numenta.htm import pool_spatial, pool_temporal

if __name__ == '__main__':
    htm = HTM()
    
    #TODO enable real data input
    data = [[1,0,1],[0,0,1]] #2d format, same dimensions as htm (for now)
    
    htm.initialize_input(data)
    
    #TODO run data over time
    for t in xrange(1):
        pool_spatial(htm)
        pool_temporal(htm, learning=True)
        
        #TODO update data array
        
        for cell in htm.cells:
            cell.clockTick()
    
    #TODO show output
    for cell in htm.cells:
        print cell
    for col in htm.columns:
        print col
    
    #TODO serialize htm state
