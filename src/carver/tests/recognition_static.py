'''
Created on Dec 7, 2010

@author: Jason Carver
'''
import unittest
from carver.htm import HTM
from carver.htm.ui.excite_history import ExciteHistory
from carver.htm.io.flashcards import FlashCards
from carver.htm.io.objectrecognize import ObjectRecognize

class TestRecognition(unittest.TestCase):


    def setUp(self):
        self.sea_anemone = [
            [1,1,0,0,1,1,0,0,1,1,0,0,1,1],
            [1,1,0,0,1,1,0,0,1,1,0,0,1,1],
            [1,1,0,0,1,1,0,0,1,1,0,0,1,1],
            [1,1,0,0,1,1,0,0,1,1,0,0,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            ]
        self.seastar = [
            [0,0,0,0,0,0,1,1,0,0,0,0,0,0],
            [0,1,0,0,0,0,1,1,0,0,0,0,1,0],
            [0,1,1,0,0,0,1,1,0,0,0,1,1,0],
            [0,0,1,1,0,0,1,1,0,0,1,1,0,0],
            [0,0,0,1,1,0,1,1,0,1,1,0,0,0],
            [0,0,0,0,1,1,1,1,1,1,0,0,0,0],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [0,0,0,0,1,1,1,1,1,1,0,0,0,0],
            [0,0,0,1,1,0,1,1,0,1,1,0,0,0],
            [0,0,1,1,0,0,1,1,0,0,1,1,0,0],
            [0,1,1,0,0,0,1,1,0,0,0,1,1,0],
            [0,1,0,0,0,0,1,1,0,0,0,0,1,0],
            [0,0,0,0,0,0,1,1,0,0,0,0,0,0],
            ]
        self.sea_cucumber = [
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,1,1,1,1,1,1,1,1,1,1,1,1,0],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [0,1,1,1,1,1,1,1,1,1,1,1,1,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            ]
        self.hermitcrab = [
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,1,1,1,1,1,1,1,1,1,1,1,1,0],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [0,1,1,1,1,1,1,1,1,1,1,1,1,0],
            [0,1,1,1,0,0,0,1,1,1,0,0,0,0],
            [1,1,0,1,1,0,1,1,0,1,1,0,0,0],
            [1,1,0,1,1,0,1,1,0,1,1,0,0,0],
            [1,0,0,0,1,0,1,0,0,0,1,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            ]
        
        pass

    def tearDown(self):
        pass

    def testFullFieldStaticImage(self):
        print_htm_state = False
        
        h = HTM(cellsPerColumn=1)
        h.initialize_input(self.sea_anemone)
        
        #learn the different static data images
        swap = FlashCards(90, self.sea_anemone, self.seastar, self.sea_cucumber, self.hermitcrab)
        h.execute(self.sea_anemone, swap.dataGenerator(), ticks=90*4*3)
        
        #run the htm network through and save the state in a history object
        swap = FlashCards(10, self.sea_anemone, self.seastar, self.sea_cucumber, self.hermitcrab)
        history = ExciteHistory(temporal=False)
        h.execute(self.sea_anemone, swap.dataGenerator(), ticks=10*4, learning=False, postTick=history.update)
        
        #label the different static data images
        recognize = ObjectRecognize()
        recognize.label('sea_anemone', history.data[-31])
        recognize.label('seastar', history.data[-21])
        recognize.label('sea_cucumber', history.data[-11])
        recognize.label('hermitcrab', history.data[-1])
        
        if print_htm_state:
            print "\n\n*************** Recognition Labeling **************\n\n"
            print history.text_graph()


        #test recognition of the different static data images
        swap.reset()
        history = ExciteHistory(temporal=False)
        h.execute(self.sea_anemone, swap.dataGenerator(), ticks=10*4, learning=False, postTick=history.update)

        if print_htm_state:
            print "\n\n*************** Recognition Testing **************\n\n"
            print history.text_graph()
        
        
        #show and test recognition data
        testnames = ['sea_anemone', 'seastar', 'sea_cucumber', 'hermitcrab']
        testdata = history.data[9:40:10]
        
        print recognize.getMatchText(testnames, testdata)
        
        for x, labelrow in enumerate(recognize.getMatchData(testnames, testdata)):
            for y, match_percent in enumerate(labelrow):
                if x == y:
                    self.assertGreaterEqual(match_percent, 0.9, 
                        msg='htm did not correctly recognize the %s (%.1f%% match)' % (
                            testnames[x], match_percent*100))
                else:
                    self.assertLessEqual(match_percent, 0.8,
                        msg='htm thought it recognized a %s, when it saw a %s (%.1f%% match)' %(
                            testnames[x], testnames[y], match_percent*100))
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testInit']
    unittest.main()
