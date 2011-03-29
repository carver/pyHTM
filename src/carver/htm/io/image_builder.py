'''
Created on Mar 23, 2011

@author: Jason
'''

from PIL import Image

class ImageBuilder(object):
    '''
    
    '''


    def __init__(self, size, dataToColor):
        '''
        @param size: a two-value element specifying the width and height of the image
        @param data: a list of data, one element for each pixel
        @param dataToColor: a method that converts from data value to color
        '''
        self.dataToColor = dataToColor
        self.img = Image.new('RGB', size)
        
    def rotate90(self):
        self.img = self.img.transpose(Image.ROTATE_90)
        
    def setData2D(self, data2D):
        return self.setData(reduce(lambda row1, row2: row1 + row2, data2D))
        
    def setData(self, data):
        '@param dimension: how many levels of iterable are there?'
        colors = map(self.dataToColor, data)
        self.img.putdata(colors)
        
    def show(self):
        return self.img.show()
    
class ColumnDisplay(object):
    def __init__(self, htm):
        width = len(htm._column_grid)
        length = len(htm._column_grid[0])
        self.imageBuilder = ImageBuilder((width, length), self.colStateColor)
        self.imageBuilder.setData(htm.columns)
        
    def show(self):
        return self.imageBuilder.show()
    
    @classmethod
    def showNow(cls, htm):
        cls(htm).show()
        
    @classmethod
    def colStateColor(cls, column):
        if column.active and column.predictedNext: #correct
            return (0,255,0)
        elif column.active: #false negative
            return (255,0,0)
        elif column.predictedNext: #false positive
            return (180,0,180) #purple
        else:
            return (0,0,0)

    
class InputCellsDisplay(object):
    def __init__(self, htm):
        self.imageBuilder = ImageBuilder((htm.width, htm.length), self.cellActiveBW)
        data = [cell for row in htm._inputCells for cell in row]
        self.imageBuilder.setData(data)
        
    def show(self):
        return self.imageBuilder.show()
        
    @classmethod
    def cellActiveBW(cls, cell):
        'A black and white representation of whether a cell is active'
        if cell.wasActive:
            return (255,255,255)
        else:
            return (0,0,0)
        
    @classmethod
    def showNow(cls, htm):
        cls(htm).show()
