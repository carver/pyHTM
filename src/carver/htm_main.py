'''
Created on Nov 26, 2010

@author: Jason Carver

'''
from carver.htm import HTM

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
    
    htm.execute(data, dataUpdate, ticks=30)
    
    #TODO show output more effectively
    for cell in htm.cells:
        print cell
    for col in htm.columns:
        print col
    
    #TODO save htm state to disk
