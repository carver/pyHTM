'''
Created on Dec 7, 2010

@author: Jason Carver
'''
import unittest
from carver.htm import HTM
from carver.htm.ui.excite_history import ExciteHistory
from carver.htm.io.objectrecognize import ObjectRecognize
from carver.htm.io.translate_input import TranslateInput
from PIL import Image
from carver.htm.io.image_builder import ImageBuilder, InputCellsDisplay,\
    ColumnDisplay, InputReflectionOverlayDisplay, ActivityOverTimeDisplay
from carver.htm.synapse import SYNAPSES_PER_SEGMENT
from carver.htm.segment import FRACTION_SEGMENT_ACTIVATION_THRESHOLD

class TestRecognitionTemporal(unittest.TestCase):


    def setUp(self):
        self.left_block = [
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [1,1,1,1,0,0,0,0,0,0,0,0,0,0],
            [1,1,1,1,0,0,0,0,0,0,0,0,0,0],
            [1,1,1,1,0,0,0,0,0,0,0,0,0,0],
            [1,1,1,1,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            ]
        self.right_block = [
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,1,1,1,1],
            [0,0,0,0,0,0,0,0,0,0,1,1,1,1],
            [0,0,0,0,0,0,0,0,0,0,1,1,1,1],
            [0,0,0,0,0,0,0,0,0,0,1,1,1,1],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            ]
        self.top_block = [
            [0,0,0,0,0,1,1,1,1,0,0,0,0,0],
            [0,0,0,0,0,1,1,1,1,0,0,0,0,0],
            [0,0,0,0,0,1,1,1,1,0,0,0,0,0],
            [0,0,0,0,0,1,1,1,1,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            ]
        self.bottom_block = [
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,1,1,1,1,0,0,0,0,0],
            [0,0,0,0,0,1,1,1,1,0,0,0,0,0],
            [0,0,0,0,0,1,1,1,1,0,0,0,0,0],
            [0,0,0,0,0,1,1,1,1,0,0,0,0,0],
            ]

    def tearDown(self):
        pass
    
    def testToyTemporalSetup(self):
        data = [
            [1,0],
            [0,0],
            ]
        h = HTM(cellsPerColumn=3)
        h.initialize_input(data)
        
        rowflip = TranslateInput(data, shift=(1,0))
        colflip = TranslateInput(data, shift=(0,1))
        
        history = ExciteHistory()
        h.execute(rowflip.dataGenerator(), ticks=20, postTick=history.update)
        h.execute(colflip.dataGenerator(), ticks=20, postTick=history.update)
        h.execute(rowflip.dataGenerator(), ticks=20, postTick=history.update)
        h.execute(colflip.dataGenerator(), ticks=20, postTick=history.update)
        
        def printCellActive(htm):
            print "cell activity:"
            for i, col in enumerate(htm.columns):
                print (
                    "column %s:" % i,
                    ' '.join(map(lambda c: '1' if c.active else '0', col.cells))
                    )
        
        h.execute(rowflip.dataGenerator(), ticks=4, learning=True,
            postTick=printCellActive)
        
        #InputCellsDisplay.showNow(h)
        
        #imagine next step
        h._imagineStimulate(h.columns)
        print "stimulation:"
        for row in h._inputCells:
            print ' '.join(map(lambda cell: '%.2f' % cell.stimulation, row))
        
        ActivityOverTimeDisplay.showNow(history.data)

    def _testTemporalImagination(self):
        h = HTM(cellsPerColumn=3)
        h.initialize_input(self.left_block, compressionFactor=2.8)
        
        #show a whole left->right pass, 5 times
        steps = 14*5
        goright = TranslateInput(self.left_block, shift=(0,1))
        h.execute(goright.dataGenerator(), ticks=steps-1)
        
        #show a whole right->left pass, 5 times
        goleft = TranslateInput(self.right_block, shift=(0,-1))
        h.execute(goleft.dataGenerator(), ticks=steps-1)
        
        #show a whole top->bottom pass, 5 times
        godown = TranslateInput(self.top_block, shift=(1,0))
        h.execute(godown.dataGenerator(), ticks=steps-1)
        
        #show a whole bottom->top pass, 5 times
        goup = TranslateInput(self.bottom_block, shift=(-1,0))
        h.execute(goup.dataGenerator(), ticks=steps-1)
        
        #TODO: test imagination automatically
        
        #do three steps of block starting left and moving right
        h.execute(dataGenerator=goright.dataGenerator(), ticks=3, 
            learning=False, postTick=InputReflectionOverlayDisplay.showNow)
        #the displays here should be mostly green and black, but a bit of purple and red is ok
        
        InputCellsDisplay.showNow(h)
        
        #imagine 9 more steps
#        for _ in xrange(9):
#            h.imagineNext()
#            
#        InputCellsDisplay.showNow(h)
            
        #downstream the last step to project back into the input,
        #see if you have a block that is on the right side
        h._imagineStimulate(h.columns)
        allStimulation = [cell.stimulation for row in h._inputCells for cell in row] 
        maxStim = max(allStimulation)
        
        white = (255,255,255)
        black = (0,0,0)
        percentSynapsesForActivation = FRACTION_SEGMENT_ACTIVATION_THRESHOLD
        def stimToRGB(stim):
            percentStimulated = stim/maxStim if maxStim else 0
            triggered = percentStimulated >= percentSynapsesForActivation
            red =  255 if triggered else 0
            green = int(percentStimulated*255)
            blue = 255 if triggered else 0
            return (red, green, blue)
        
        img = ImageBuilder([h.inputWidth, h.inputLength], stimToRGB)
        img.setData(allStimulation)
        img.show()
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testInit']
    unittest.main()
