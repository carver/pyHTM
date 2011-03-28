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
